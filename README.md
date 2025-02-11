# ATS (Applicant Tracking System)

An AI-powered **Applicant Tracking System** that automates **resume screening, candidate scoring, personality & aptitude assessments**, and **approval/rejection system** to streamline hiring.

---

## Features
- ✅ **Resume Parsing & Scoring** – Extracts candidate details & assigns scores.  
- ✅ **Personality & Aptitude Tests** – Evaluates candidates based on AI-driven assessments.  
- ✅ **Overall Candidate Rating** – Generates an **aggregated score** for better hiring decisions.  
- ✅ **Auto-Approve & Reject** – Filters candidates based on pre-defined criteria.  
- ✅ **REST API Support** – Easily integrates with external HR tools.  

---

# 🛠️ Installation Guide
Follow these steps to set up the project on your local machine.

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vrindtime/ats.git
cd ats
```

## 2️⃣ Set Up a Virtual Environment
```bash
python -m venv .venv
venv\Scripts\activate  # Linux: source .venv/bin/activate
```

## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables with `django-environ`
Since we are using **`django-environ`**, follow these steps:

1. **Install `django-environ`** (if not already installed)
   ```bash
   pip install django-environ
   ```
   
2. **Create a `.env` file** in the project's root directory:
   ```ini
   SECRET_KEY='your-secret-key'
   ENVIRONMENT=development
   RESUME_PARSER_API_KEY='your-api-key-here'
   ```

3. **Modify `settings.py` to load environment variables**:
   ```python
   # Note this steps are already done and you can skip these, but check in case of failure
   import environ

   # Initialize environ
   env = environ.Env()
   environ.Env.read_env()  # Read from .env file

   SECRET_KEY = env('SECRET_KEY')
   DEBUG = env.bool('DEBUG', default=False)
   RESUME_PARSER_API_KEY = env('RESUME_PARSER_API_KEY')
   ```

---

## 5️⃣ Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

---

## 7️⃣ Run the Development Server
```bash
python manage.py runserver
```
Now, visit **`http://127.0.0.1:8000/`** in your browser. 🎉

---

## 🔑 Using the API Key in Code
You can access the API key inside Django views, models, or services like this:
```python
import requests
from django.conf import settings

API_KEY = settings.RESUME_PARSER_API_KEY

headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get("https://api.resumeparser.com/parse", headers=headers)
```

# 🔗 ATS Software URL Routes

This document lists all the URL routes used in the ATS software, including their HTTP methods and descriptions.

## Root URLs
| URL | Method | Description |
|------|--------|-------------|
| `/admin/` | - | Admin panel (hidden behind a honeypot for security) |
| `/backend/` | - | Main admin panel |
| `/` | GET | Home page |
| `/accounts/` | - | User account-related routes |
| `/resume/` | - | Resume-related routes |
| `/personality/` | - | Personality test-related routes |
| `/aptitude/` | - | Aptitude test-related routes |

## Resume URLs
| URL | Method | Description |
|------|--------|-------------|
| `/dashboard/` | GET | Resume dashboard |
| `/upload/` | POST | Upload a resume |
| `/resume/<int:resume_id>/` | GET | View resume details |
| `/add-job/` | POST | Add a job posting |
| `/delete_resume/<int:id>/` | DELETE | Delete a resume |

## Dashboard URLs
| URL | Method | Description |
|------|--------|-------------|
| `/login/` | GET, POST | Login page |
| `/logout/` | GET | Logout user |
| `/dashboard/` | GET | Admin dashboard |
| `/approve/<str:id>/` | POST | Approve a user |
| `/reject/<str:id>/` | POST | Reject a user |

## Home URLs
| URL | Method | Description |
|------|--------|-------------|
| `/` | GET | Home page |
| `/start/` | GET | Start a test |
| `/clear/` | GET | Clear cache |
| `/result/` | GET | Show test results |
| `/delete/<str:id>/` | DELETE | Delete a user |

## Personality Test URLs
| URL | Method | Description |
|------|--------|-------------|
| `/personality/dashboard/` | GET | Personality test dashboard |
| `/personality/add-question/` | POST | Add a new personality test question |
| `/personality/add-choice/<int:question_id>/` | POST | Add a choice to a personality question |
| `/personality/test/` | GET | Start the personality test |
| `/personality/add-category/` | POST | Add a personality category |
| `/personality/edit-question/<int:id>/` | POST | Edit a personality question |
| `/personality/delete-question/<int:id>/` | DELETE | Delete a personality question |
| `/personality/delete-choice/<int:id>/` | DELETE | Delete a personality choice |

## Aptitude Test URLs
| URL | Method | Description |
|------|--------|-------------|
| `/aptitude/dashboard/` | GET | Aptitude test dashboard |
| `/aptitude/addQuestions/` | POST | Add aptitude test questions |
| `/aptitude/addCategory/` | POST | Add an aptitude category |
| `/aptitude/test/` | GET | Start the aptitude test |
| `/aptitude/submit-test/` | POST | Submit the aptitude test |
| `/aptitude/edit_aptitude/<int:id>/` | POST | Edit an aptitude test question |
| `/aptitude/delete_aptitude/<int:id>/` | DELETE | Delete an aptitude test question |

---

## License
This project is licensed under the MIT License.

---

