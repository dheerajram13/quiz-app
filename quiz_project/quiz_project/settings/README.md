# Django Settings Structure

This project uses a split settings configuration to manage different environments (development, production).

## Structure

```
settings/
├── __init__.py      # Auto-detects environment and imports appropriate settings
├── base.py          # Common settings shared across all environments
├── dev.py           # Development-specific settings
└── prod.py          # Production-specific settings
```

## Usage

### Development Environment (Default)

By default, the application uses development settings:

```bash
python manage.py runserver
```

Or explicitly set the environment:

```bash
export DJANGO_ENV=dev
python manage.py runserver
```

### Production Environment

To use production settings, set the `DJANGO_ENV` environment variable:

```bash
export DJANGO_ENV=prod
python manage.py runserver
```

## Environment Variables

### Development (.env file)

For development, you can use a `.env` file with minimal configuration:

```env
# Optional for dev (has a default fallback)
DJANGO_SECRET_KEY=your-dev-secret-key

# Development uses DEBUG=True by default
# Development uses SQLite by default
```

### Production (Environment Variables)

For production, you **must** set these environment variables:

```env
# Required
DJANGO_ENV=prod
DJANGO_SECRET_KEY=your-production-secret-key-keep-this-secret
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (PostgreSQL recommended)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=quiz_db
DB_USER=quiz_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@quizapp.com

# Security (optional, defaults provided)
SECURE_SSL_REDIRECT=True
```

## Key Differences Between Environments

### Development (dev.py)
- DEBUG = True
- SQLite database
- Permissive CORS settings
- Debug toolbar enabled
- Console email backend
- Verbose logging (DEBUG level)
- Security settings disabled

### Production (prod.py)
- DEBUG = False
- PostgreSQL database (recommended)
- Strict CORS settings
- SMTP email backend
- INFO level logging with larger log files
- Full security settings enabled:
  - SSL redirect
  - HSTS enabled
  - Secure cookies
  - Security headers

## Running Django Commands

All Django commands work the same way, just set the environment first:

```bash
# Development
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Production
export DJANGO_ENV=prod
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## Deployment

For production deployment (e.g., with Gunicorn):

```bash
export DJANGO_ENV=prod
gunicorn quiz_project.wsgi:application --bind 0.0.0.0:8000
```

Or with environment variable inline:

```bash
DJANGO_ENV=prod gunicorn quiz_project.wsgi:application --bind 0.0.0.0:8000
```

## Testing

To test if settings are loaded correctly:

```bash
# Test development settings
python manage.py check

# Test production settings (may fail without required env vars)
DJANGO_ENV=prod python manage.py check
```

## Notes

- The `__init__.py` file automatically detects the environment based on `DJANGO_ENV`
- If `DJANGO_ENV` is not set, it defaults to development
- Production settings will raise `ImproperlyConfigured` errors if required variables are missing
- Never commit your `.env` file or production secrets to version control
