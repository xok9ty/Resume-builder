from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="builder_user_groups", 
        related_query_name="builder_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="builder_user_permissions",  
        related_query_name="builder_user",
    )

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва шаблону')
    description = models.TextField(verbose_name='Опис шаблону')
    thumbnail = models.ImageField(upload_to='template_thumbnails/', verbose_name='Мініатюра')
    preview_image = models.ImageField(upload_to='template_previews/', verbose_name='Зображення прев\'ю')  # ВИПРАВЛЕНО
    html_file = models.FileField(upload_to='templates/', verbose_name='HTML файл шаблону')
    css_file = models.FileField(upload_to='templates/css/', verbose_name='CSS файл шаблону', blank=True, null=True)
    is_premium = models.BooleanField(default=False, verbose_name='Преміум шаблон')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Шаблон резюме'
        verbose_name_plural = 'Шаблони резюме'

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', verbose_name='Користувач')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Шаблон')
    title = models.CharField(max_length=100, verbose_name='Назва резюме')
    is_public = models.BooleanField(default=False, verbose_name='Публічне')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_info', verbose_name='Резюме')
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='По батькові')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=200, blank=True, verbose_name='Адреса')
    photo = models.ImageField(upload_to='resume_photos/', blank=True, null=True, verbose_name='Фото')
    summary = models.TextField(blank=True, verbose_name='Про себе')

    class Meta:
        verbose_name = 'Особиста інформація'
        verbose_name_plural = 'Особиста інформація'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experiences', verbose_name='Резюме')
    company = models.CharField(max_length=100, verbose_name='Компанія')
    position = models.CharField(max_length=100, verbose_name='Посада')
    start_date = models.DateField(verbose_name='Дата початку')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата завершення')
    currently_working = models.BooleanField(default=False, verbose_name='Працюю зараз')
    description = models.TextField(blank=True, verbose_name='Опис')

    class Meta:
        verbose_name = 'Досвід роботи'
        verbose_name_plural = 'Досвід роботи'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations', verbose_name='Резюме')
    institution = models.CharField(max_length=200, verbose_name='Навчальний заклад')
    degree = models.CharField(max_length=100, verbose_name='Ступінь')
    field_of_study = models.CharField(max_length=100, verbose_name='Спеціальність')
    start_date = models.DateField(verbose_name='Дата початку')
    end_time = models.DateField(blank=True, null=True, verbose_name='Дата завершення')
    currently_studying = models.BooleanField(default=False, verbose_name='Навчаюсь зараз')
    description = models.TextField(blank=True, verbose_name='Опис')

    class Meta:
        verbose_name = 'Освіта'
        verbose_name_plural = 'Освіта'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} at {self.institution}"

class Skill(models.Model):
    SKILL_LEVELS = (
        ('beginner', 'Початківець'),
        ('intermediate', 'Середній'),
        ('advanced', 'Просунутий'),
        ('expert', 'Експерт'),
    )
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills', verbose_name='Резюме')
    name = models.CharField(max_length=100, verbose_name='Назва навички')
    level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='intermediate', verbose_name='Рівень')
    category = models.CharField(max_length=50, blank=True, verbose_name='Категорія')

    class Meta:
        verbose_name = 'Навичка'
        verbose_name_plural = 'Навички'

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Language(models.Model):
    LANGUAGE_LEVELS = (
        ('a1', 'A1 - Початковий'),
        ('a2', 'A2 - Елементарний'),
        ('b1', 'B1 - Середній'),
        ('b2', 'B2 - Вище середнього'),
        ('c1', 'C1 - Просунутий'),
        ('c2', 'C2 - Вільний'),
        ('native', 'Рідна'),
    )
    
    resume = models.ForeignKey( Resume, on_delete=models.CASCADE, related_name='languages', verbose_name='Резюме' )
    name = models.CharField(max_length=50, verbose_name='Мова')
    level = models.CharField( max_length=10, choices=LANGUAGE_LEVELS, verbose_name='Рівень')

    class Meta:
        verbose_name = 'Мова'
        verbose_name_plural = 'Мови'

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Certificate(models.Model):
    resume = models.ForeignKey( Resume, on_delete=models.CASCADE, related_name='certificates', verbose_name='Резюме')
    name = models.CharField(max_length=200, verbose_name='Назва сертифікату')
    issuing_organization = models.CharField(max_length=200, verbose_name='Організація')
    issue_date = models.DateField(verbose_name='Дата отримання')
    expiration_date = models.DateField(blank=True, null=True, verbose_name='Термін дії')
    credential_id = models.CharField(max_length=100, blank=True, verbose_name='ID сертифікату')
    credential_url = models.URLField(blank=True, verbose_name='Посилання')

    class Meta:
        verbose_name = 'Сертифікат'
        verbose_name_plural = 'Сертифікати'
        ordering = ['-issue_date']

    def __str__(self):
        return self.name

class Announcement(models.Model):

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    author = models.ForeignKey( User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    is_active = models.BooleanField(default=True, verbose_name='Активне')

    class Meta:
        verbose_name = 'Оголошення'
        verbose_name_plural = 'Оголошення'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ResumeExport(models.Model):

    EXPORT_FORMATS = (
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('html', 'HTML'),
    )
    
    resume = models.ForeignKey( Resume, on_delete=models.CASCADE, related_name='exports', verbose_name='Резюме' )
    format = models.CharField( max_length=10, choices=EXPORT_FORMATS, verbose_name='Формат' )
    file = models.FileField( upload_to='resume_exports/', verbose_name='Файл')
    exported_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата експорту')

    class Meta:
        verbose_name = 'Експорт резюме'
        verbose_name_plural = 'Експорти резюме'
        ordering = ['-exported_at']

    def __str__(self):
        return f"{self.resume.title} ({self.get_format_display()})"