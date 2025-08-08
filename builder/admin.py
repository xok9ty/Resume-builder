from django.contrib import admin
from builder.models import User, ResumeTemplate, Resume, PersonalInfo, WorkExperience, Education, Skill, Language, Certificate, Announcement, ResumeExport


admin.site.register(User)
admin.site.register(ResumeTemplate)
admin.site.register(Resume)
admin.site.register(PersonalInfo)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Announcement)
admin.site.register(ResumeExport)
