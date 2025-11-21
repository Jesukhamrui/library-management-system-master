**Library Management System — Documentation**

Library Management System - Complete Documentation

Project Overview
This document provides comprehensive documentation for the Library Management System — a Django-based web application originally implemented with MySQL (dump in `source/book.sql`) and updated to run on modern Python/Django environments. The project exposes book listings, comments, loans, reserves, and basic user authentication.

Purpose
The Library Management System demonstrates a small-scale library application with real-world features: searching and listing books, recording loans, adding comments, and managing reserves. The repository includes a legacy MySQL dump and a development-friendly SQLite fallback so you can run and test the application quickly.

Technology Stack
• Backend Framework: Django (project updated for Django 5.x; validated with Django 5.2.8)
• Python: 3.13.7 (targeted/tested)
• Database: MySQL (production/legacy) — `source/book.sql` provided. SQLite3 fallback for local development.
• Frontend: HTML5, CSS, JavaScript (Materialize + custom static assets)
• Optional: Docker (recommended for isolated MySQL testing)

Key Features
• Book listing, search and detail pages
• User authentication and profile editing
• Comments on books (add/delete)
• Loans and reserves management (staff vs reader flows)
• SQLite fallback to run without MySQL; defensive handling to avoid 500s when legacy tables are absent

Architecture Pattern
The project follows Django's MVT (Model-View-Template) architecture:
• Model: `library/models.py` (inspectdb-style models for legacy schema; many are `managed = False`)
• View: `library/views.py` — handles requests, business logic, and defensive DB error handling
• Template: HTML in `templates/` renders dynamic content

Installation and Setup
Prerequisites
• Python 3.13.7
• pip
• Virtual environment (recommended)
• Optional: MySQL server (for using `source/book.sql`) or Docker (to run MySQL container locally)

Installation Steps (Windows PowerShell)
Step 1: Clone or open the repository (you already have it locally)
Step 2: Create/activate virtual environment
```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```
Step 3: Install dependencies
```powershell
pip install -r requirements.txt
```
Step 4: Run database migrations (SQLite fallback; recommended for quick start)
```powershell
# $env:DJANGO_USE_SQLITE = '1'   # ensure SQLite fallback is enabled for the session
$env:DJANGO_USE_SQLITE = '1'
python manage.py migrate
python manage.py createsuperuser   # optional: create admin account
python manage.py runserver
```
Open http://127.0.0.1:8000/ to view the app.

Using the Original MySQL Dump (`source/book.sql`)
If you want the application to reflect the original dataset, import `source/book.sql` into a MySQL instance and point Django to it.

Option A — Import into an existing MySQL server (PowerShell friendly)
1) Create database and user (adjust names/host/password):
```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS book CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci; CREATE USER IF NOT EXISTS 'lmsuser'@'127.0.0.1' IDENTIFIED BY 'strongpassword'; GRANT ALL PRIVILEGES ON book.* TO 'lmsuser'@'127.0.0.1'; FLUSH PRIVILEGES;"
```
2) Import the dump (PowerShell):
```powershell
Get-Content .\source\book.sql -Raw | mysql -u lmsuser -p -h 127.0.0.1 -P 3306 book
```
3) Configure Django to use MySQL (either edit `lms/settings.py` or set environment variables):
```powershell
# $env:DJANGO_USE_SQLITE = ''   # unset or set to empty so MySQL is used
$env:DJANGO_USE_SQLITE = ''
$env:DJANGO_DB_NAME = 'book'
$env:DJANGO_DB_USER = 'lmsuser'
$env:DJANGO_DB_PASSWORD = 'strongpassword'
$env:DJANGO_DB_HOST = '127.0.0.1'
$env:DJANGO_DB_PORT = '3306'
python manage.py migrate
python manage.py runserver
```

Notes on PowerShell redirection: the common Unix `< file.sql` redirection can be done via `cmd /c` if needed:
```powershell
cmd /c "mysql -u lmsuser -p -h 127.0.0.1 book < source\\book.sql"
```

Option B — Use Docker (isolated, recommended if you do not want to alter host MySQL)
1) Run a MySQL container and import dump:
```powershell
docker run --name lms-mysql -e MYSQL_ROOT_PASSWORD=rootpw -e MYSQL_DATABASE=book -p 3306:3306 -d mysql:5.7
# Wait for MySQL to initialize, then copy and import
docker cp .\source\book.sql lms-mysql:/book.sql
docker exec -i lms-mysql bash -c "mysql -u root -prootpw book < /book.sql"
```
2) Point Django to `127.0.0.1:3306` and use the `root` or created user credentials.

API / Data Notes
• The project uses database models and the existing SQL dump: `books`, `comments`, `loans`, `reserves`, `storages`, and `auth_user`.

Security Considerations
Current Risks in repository (as found)
• Hardcoded DB credentials in `lms/settings.py` may exist in some setups — move secrets to environment variables.
• `DEBUG = True` in development exposes sensitive tracebacks — always set `DEBUG = False` in production.
• `SECRET_KEY` should be stored in environment variables or a secrets manager for production.
• MySQL user host restrictions: create users bound to the correct host (`127.0.0.1` vs `localhost` differences).

Performance Recommendations
• Implement caching (Django cache framework, Redis) for frequently requested lists (books/comments).
• Move heavyweight or recurring database operations to background tasks (Celery + Redis) if workload grows.
• Convert legacy `inspectdb` models to managed models with migrations so Django can better optimize queries.

Deployment Guide (Production Checklist)
1) Prepare app
• Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
• Move DB credentials and `SECRET_KEY` to environment variables.
• Run `python manage.py collectstatic`.
2) Choose hosting
• VPS (DigitalOcean, AWS EC2), PaaS (Heroku), or App Platform.
3) Web server
• Use Gunicorn or uWSGI behind Nginx (reverse proxy).
• Set up TLS (Let's Encrypt).
4) Database
• Use managed MySQL or PostgreSQL for production.
• Run migrations against production DB.
5) Logging & Monitoring
• Add Sentry or similar error tracking.
• Configure log rotation and monitoring.



MySQL Authentication Errors (1045)
• Cause: wrong username/host/password or missing privileges.
• Fix: ensure the MySQL user exists for the specific host (create `user@'127.0.0.1'` if Django connects to 127.0.0.1). Grant required privileges: `GRANT ALL PRIVILEGES ON book.* TO 'user'@'127.0.0.1';`.

PowerShell file import issues
• Use `Get-Content -Raw | mysql ...` or `cmd /c "mysql ... < file.sql"` when importing SQL dumps on Windows PowerShell.

Changes Made by Maintainer (what was updated in this repository)
• Added SQLite fallback configurable with `DJANGO_USE_SQLITE` to run without MySQL.
• Registered `PyMySQL` shim in `lms/__init__.py` for Windows compatibility.
• Added `lms.middleware.DBUnavailableMiddleware` to provide a friendly response when DB is unreachable.
• Converted several views (`comments`, `reserves`, `book`, `loans`, `books`) to catch `OperationalError` and return safe empty lists rather than allowing template-time DB exceptions.
• Fixed `ProfileForm` to use Django's `User` model so `profile_edit` works with `request.user`.
• Updated templates to use `{% load static %}` and added small static assets for improved UI interaction.

Contributing
• If you want to improve the code, consider converting `library/models.py` from `inspectdb` output into managed models (remove `managed = False` where appropriate) and add migrations with `makemigrations`/`migrate`.
• For larger refactors (schema changes), create feature branches and open pull requests.

Appendix
Project structure (top-level):
• `lms/` — Django project settings and WSGI
• `library/` — main application (models, views, forms, urls)
• `templates/` — HTML templates
• `static/` — static assets (CSS, JS, images)
• `source/book.sql` — legacy MySQL dump with schema + seed data

Version Information
• Python: 3.13.7 (target)
• Django: 5.x (validated with 5.2.8)

---
End of documentation.
