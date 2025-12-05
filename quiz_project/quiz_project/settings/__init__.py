"""
Settings package for quiz_project.
Automatically imports the correct settings module based on the DJANGO_ENV environment variable.

Environment variables:
- DJANGO_ENV: Set to 'dev', 'prod', or 'production' (defaults to 'dev')
  * 'dev' or 'development' -> uses settings.dev
  * 'prod' or 'production' -> uses settings.prod
"""

import os

# Get the environment from DJANGO_ENV variable (defaults to 'dev')
environment = os.getenv('DJANGO_ENV', 'dev').lower()

# Map environment names to settings modules
if environment in ['prod', 'production']:
    from .prod import *
    print(f"Loading PRODUCTION settings (DJANGO_ENV={environment})")
elif environment in ['dev', 'development']:
    from .dev import *
    print(f"Loading DEVELOPMENT settings (DJANGO_ENV={environment})")
else:
    # Default to development if unknown environment
    from .dev import *
    print(f"Unknown DJANGO_ENV '{environment}', defaulting to DEVELOPMENT settings")
