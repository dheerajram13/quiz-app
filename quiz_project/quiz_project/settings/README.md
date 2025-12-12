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

## Database Routers

This project includes database routers for advanced multi-database configurations. See [quiz_project/db_routers.py](../db_routers.py) for implementation details.

### Available Routers

1. **PrimaryReplicaRouter** - Read/write splitting
   - All writes go to `default` (primary)
   - All reads go to `replica` database
   - Improves performance by distributing read load

2. **AppBasedRouter** - Route by Django app
   - Different apps use different databases
   - Useful for microservices architecture
   - Configure with `APP_DB_ROUTING` setting

3. **ModelBasedRouter** - Route by specific models
   - Fine-grained control per model
   - Configure with `MODEL_DB_ROUTING` setting
   - Example: Analytics models to analytics DB

4. **HybridRouter** - Combines app-based + read/write splitting
   - Best of both worlds
   - Configure with `HYBRID_DB_ROUTING` setting

### Using Database Routers

To enable a router, uncomment the appropriate configuration in [base.py](base.py):

```python
# Example: Enable read/write splitting
DATABASE_ROUTERS = ['quiz_project.db_routers.PrimaryReplicaRouter']

# Configure databases in dev.py or prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'HOST': 'primary.db.server.com',
        ...
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'HOST': 'replica.db.server.com',
        ...
    }
}
```

See [db_examples.py](db_examples.py) for complete configuration examples.

### Working with Multiple Databases

```bash
# Run migrations on specific database
python manage.py migrate --database=default
python manage.py migrate --database=analytics_db

# Manually specify database in queries
User.objects.using('replica').all()
quiz.save(using='default')

# Database routing happens automatically with routers configured
Quiz.objects.all()  # Reads from replica automatically
quiz.save()         # Writes to primary automatically
```

### Testing with Multiple Databases

```bash
# Test database creation is automatic
python manage.py test

# Flush specific database
python manage.py flush --database=default
```

## Notes

- The `__init__.py` file automatically detects the environment based on `DJANGO_ENV`
- If `DJANGO_ENV` is not set, it defaults to development
- Production settings will raise `ImproperlyConfigured` errors if required variables are missing
- Never commit your `.env` file or production secrets to version control
- Database routers are evaluated in the order they appear in `DATABASE_ROUTERS`
- For multi-database setups, ensure proper replication is configured at the database level
