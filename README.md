# Resume-builder

## Description  
**Resume-builder** is a web application that allows users to quickly create professional resumes.  
It provides ready-to-use templates, an intuitive interface for entering data, and export options in multiple formats (PDF, DOCX, etc.).  
The project is built with **Django**.

---

## Requirements  
Before installation, make sure your system meets the following requirements:

- Python 3.8 or higher  
- Django (version specified in `requirements.txt`)  
- SQLite (default) or another compatible database  
- pip — for dependency installation  
- Virtual environment `venv`

---

## Features  
✅ Easy-to-use interface for data entry  
✅ Add sections: education, work experience, skills, certifications  
✅ Automatically generate resumes in PDF/HTML format  
✅ Multiple design templates available  
✅ Edit and save user data  
✅ Responsive design for all devices  

---

## Installation

1. Install the required libraries:
   ```
   pip install django
   ```
   
2. Clone the repository:
   ```
   git clone https://github.com/xok9ty/dj_project.git
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   # Windows use `venv\Scripts\activate`
   # MacOS use `source venv\Scripts\activate`
   ```

4. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the applicatoin at http://127.0.0.1:8000/

---

## Usage  

Once the server is running, follow these steps:

1. **Open the homepage**  
   Navigate to: http://127.0.0.1:8000


2. **Create a user account**  
- Click on **Sign Up** to register a new account, or  
- Log in if you already have one.

3. **Fill in your resume data**  
Add the following sections:
- Personal information  
- Education  
- Work experience  
- Skills  
- Certifications (optional)

4. **Choose a resume template**  
Browse available templates and select the one that fits your style.

5. **Preview your resume**  
Check how your resume looks in the chosen format before downloading.

6. **Export your resume**  
Click **Export** to download your completed resume as:
- PDF  
- DOCX  


---

