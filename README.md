# KanMind

KanMind is a full-stack project composed of a Django backend and a static frontend. The backend exposes the application logic and REST API, while the frontend is a vanilla JavaScript app that communicates with the API.

This repository is intended to be run locally during development. The project uses SQLite by default for the database and relies on environment variables for Django configuration.

---

## Project structure

- `backend/` — Django backend project and API
- `frontend/` — static frontend application (HTML, CSS, JavaScript)
- `db.sqlite3` — local SQLite database
- `.env` — environment variables for local development
- `.venv/` — local Python virtual environment

---

## Requirements

Before starting the project, make sure you have the following installed:

- Python 3.11+
- pip
- virtualenv / venv support
- Git
- VS Code (recommended)
- Optional: Live Server extension for the frontend

The backend dependencies are pinned in `backend/requirements.txt`:

```text
asgiref==3.12.1
Django==6.1
django-cors-headers==4.9.0
djangorestframework==3.18.0
drf-nested-routers==0.95.3
flake8==7.3.0
mccabe==0.7.0
pycodestyle==2.14.0
pyflakes==3.4.0
python-dotenv==1.2.2
sqlparse==0.6.0
tzdata==2026.3
```

---

## Environment variables

The backend expects a `.env` file in the project root with at least the following values:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
```

Notes:

- `DJANGO_SECRET_KEY` is required by Django.
- `DJANGO_DEBUG` should be set to `True` for local development.
- In this project, the settings file loads environment variables using `python-dotenv`.

If `.env` is missing, Django may fail to start properly because `SECRET_KEY` is read from the environment.

---

## Quick start

### 1) Start the backend

From the project root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On macOS/Linux, use:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The backend normally runs at:

- http://127.0.0.1:8000

---

### 2) Start the frontend

There are two supported ways to run the frontend locally:

#### Option A: VS Code Live Server (recommended)

1. Open the `frontend/` folder in VS Code.
2. Open `frontend/index.html`.
3. Right-click the file and choose `Open with Live Server`.

This is the intended development workflow for this project.

#### Option B: Python HTTP server

```bash
cd frontend
python -m http.server 5500
```

Then open:

- http://127.0.0.1:5500

---

## Important project-specific notes

### Django settings and CORS

The backend includes CORS configuration for local development. The list of allowed frontend origins is defined in `backend/kan_mind/settings.py` and includes addresses such as:

- `http://127.0.0.1:8000`
- `http://192.168.178.130:5500`
- `http://172.20.160.1:5500`

If you run the frontend from a different local address or port, you may need to update `CORS_ALLOWED_ORIGINS`.

### Authentication

The backend uses Django REST Framework with token authentication.

- Default permission is set to `IsAuthenticated`.
- Authentication endpoints are exposed under the API routes.
- User registration and login are handled through the `user_auth_app` API modules.

### Database

The project uses SQLite by default:

- `backend/db.sqlite3`

This makes local development easy and avoids needing a separate database server.

### API routing

The backend is organized into two major API groups:

- `user_auth_app.api.urls`
- `board_app.api.urls`

The root URL configuration is defined in `backend/kan_mind/urls.py`.

---

## Typical development workflow

1. Activate the virtual environment.
2. Install dependencies from `backend/requirements.txt`.
3. Create or update the `.env` file.
4. Run migrations.
5. Start Django with `python manage.py runserver`.
6. Start the frontend with Live Server or a simple HTTP server.
7. Use the browser to interact with the app.

---

## Troubleshooting

### Django does not start

Check the following:

- Python virtual environment is activated
- `pip install -r requirements.txt` was completed successfully
- `.env` contains `DJANGO_SECRET_KEY`
- You are inside the `backend` folder when running Django commands

### Frontend cannot reach the API

Check:

- the backend is running on port 8000
- the frontend is served from an allowed origin in `CORS_ALLOWED_ORIGINS`
- the API URLs match the frontend configuration

### Database errors

Run:

```bash
python manage.py migrate
```

If the database is inconsistent or stale, recreate it with caution:

```bash
rm db.sqlite3
python manage.py migrate
```

---

## Summary

The project is designed for local development with:

- Django backend on port `8000`
- static frontend on port `5500` (via Live Server or simple HTTP server)
- SQLite database for simplicity
- environment variables for security configuration

This README covers the required setup and startup flow for running the project locally.
