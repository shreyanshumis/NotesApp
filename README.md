# Scribe NotesApp

A private, Google-authenticated notes app built with Django.

Scribe is designed to feel like a leather-bound journal brought into the digital world: warm paper tones, royal purple accents, soft animated background details, and a quiet writing-focused interface.

## Features

- Google SSO login with `django-allauth`
- Per-user note privacy: users only see, edit, delete, share, and export their own notes
- Create, read, update, and delete notes
- Search notes by title or content
- Share notes as PDF or image
- Export/download notes as PDF or image
- Django admin support
- Light and dark mode
- Soft background animations and custom visual styling
- Render-ready deployment setup

## Tech Stack

- Python 3.13
- Django 5
- django-allauth
- SQLite for local development
- PostgreSQL on Render
- WhiteNoise for static files
- Gunicorn + Uvicorn for production serving
- Pillow and ReportLab for image/PDF exports

## Project Structure

```txt
NotesApp/
├── journal/              # Django project settings and URLs
├── notes/                # Notes app: models, views, forms, exports, tests
├── static/               # CSS and JavaScript
├── templates/            # Django templates
├── build.sh              # Render build script
├── render.yaml           # Render Blueprint config
├── requirements.txt
├── manage.py
└── .env.example
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/shreyanshumis/NotesApp.git
cd NotesApp
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver 127.0.0.1:8001
```

Open:

```txt
http://127.0.0.1:8001/
```

## Environment Variables

Use `.env.example` as a reference.

Required for production:

```txt
SECRET_KEY=your-django-secret-key
DEBUG=False
RENDER=true
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

Render automatically provides `DATABASE_URL` if you use the included `render.yaml` database setup.

### Important Secret Key Note

`SECRET_KEY` is Django’s secret key. It is not the same as the Google OAuth secret.

Generate a Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Use it like this on Render:

```txt
KEY: SECRET_KEY
VALUE: generated-django-secret-key
```

Google credentials are separate:

```txt
KEY: GOOGLE_OAUTH_CLIENT_ID
VALUE: your-google-oauth-client-id

KEY: GOOGLE_OAUTH_CLIENT_SECRET
VALUE: your-google-oauth-client-secret
```

Never commit real secrets to GitHub.

## Google SSO Setup

Go to the Google Cloud Console:

```txt
APIs & Services → Credentials
```

Create an OAuth Client ID:

```txt
Application type: Web application
```

Add this authorized redirect URI for Render:

```txt
https://scribe-notesapp.onrender.com/accounts/google/login/callback/
```

For local testing, also add:

```txt
http://127.0.0.1:8001/accounts/google/login/callback/
http://localhost:8001/accounts/google/login/callback/
```

The redirect URI must match exactly, including the trailing slash.

After creating the OAuth client, copy:

- Client ID → `GOOGLE_OAUTH_CLIENT_ID`
- Client Secret → `GOOGLE_OAUTH_CLIENT_SECRET`

If a client secret is ever pasted publicly or shared accidentally, rotate it in Google Cloud.

## Render Deployment

This repo includes:

- `render.yaml`
- `build.sh`
- `.python-version`

The Render build command is:

```bash
bash ./build.sh
```

The Render start command is:

```bash
python -m gunicorn journal.asgi:application -k uvicorn.workers.UvicornWorker
```

The build script:

1. Installs dependencies
2. Runs `collectstatic`
3. Runs database migrations

Render health checks use:

```txt
/healthz/
```

Example:

```txt
https://scribe-notesapp.onrender.com/healthz/
```

It returns:

```json
{
  "status": "ok",
  "commit": "abcdef1"
}
```

The `commit` value helps confirm which Git commit Render is actually serving.

## Render Environment Variables

In Render:

```txt
Service → Environment → Edit
```

Add:

```txt
SECRET_KEY=your-django-secret-key
DEBUG=False
RENDER=true
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

If using the included Blueprint, `DATABASE_URL` is provided by the Render PostgreSQL database.

After changing environment variables:

```txt
Manual Deploy → Clear build cache & deploy
```

## Common Troubleshooting

### Render is showing an old page

Check:

```txt
https://scribe-notesapp.onrender.com/healthz/
```

If the commit is old, redeploy the latest commit from Render.

Use:

```txt
Manual Deploy → Clear build cache & deploy
```

Also confirm Render is connected to the `main` branch.

### CSS or styles are missing

Make sure the build script ran successfully:

```bash
python manage.py collectstatic --no-input
```

The app uses WhiteNoise to serve static files in production.

### Google login says credentials are not set

Make sure these exist in Render environment variables:

```txt
GOOGLE_OAUTH_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET
```

Then redeploy.

### Google login gives `redirect_uri_mismatch`

Add the exact redirect URI to Google Cloud:

```txt
https://scribe-notesapp.onrender.com/accounts/google/login/callback/
```

For local development:

```txt
http://127.0.0.1:8001/accounts/google/login/callback/
```

### Render build fails with `SECRET_KEY must be set`

Add a Django secret key to Render:

```txt
KEY: SECRET_KEY
VALUE: generated-django-secret-key
```

Generate one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Running Tests

```bash
python manage.py test
```

Run Django checks:

```bash
python manage.py check
```

## License

This project is for learning and portfolio use. Add a license file if you plan to distribute or open-source it formally.
