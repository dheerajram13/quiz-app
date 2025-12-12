"""
Example multi-database configurations for quiz_project.

This file provides example DATABASES configurations for various use cases.
Copy the relevant configuration to your dev.py or prod.py file and customize.

WARNING: This file is for reference only and is not imported by Django.
"""

# ============================================================================
# Example 1: Single Database (Current Default)
# ============================================================================
DATABASES_SINGLE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# ============================================================================
# Example 2: Primary-Replica Setup (Read/Write Splitting)
# ============================================================================
# Use with: PrimaryReplicaRouter
# Benefits: Distribute read load across replicas, improve performance

DATABASES_PRIMARY_REPLICA = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'primary.db.server.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user_readonly',
        'PASSWORD': 'password',
        'HOST': 'replica.db.server.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'options': '-c default_transaction_read_only=on'  # Ensure read-only
        }
    }
}

# Required router configuration:
# DATABASE_ROUTERS = ['quiz_project.db_routers.PrimaryReplicaRouter']


# ============================================================================
# Example 3: Multiple Replicas with Load Balancing
# ============================================================================
# Use with: Custom router or PrimaryReplicaRouter with connection pooling

DATABASES_MULTIPLE_REPLICAS = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'primary.db.server.com',
        'PORT': '5432',
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user_readonly',
        'PASSWORD': 'password',
        'HOST': 'replica1.db.server.com',  # Could use DNS round-robin or load balancer
        'PORT': '5432',
    },
    'replica2': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user_readonly',
        'PASSWORD': 'password',
        'HOST': 'replica2.db.server.com',
        'PORT': '5432',
    }
}


# ============================================================================
# Example 4: App-Based Database Separation
# ============================================================================
# Use with: AppBasedRouter
# Benefits: Separate concerns, independent scaling, data isolation

DATABASES_APP_BASED = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'analytics_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics_db',
        'USER': 'analytics_user',
        'PASSWORD': 'password',
        'HOST': 'analytics.db.server.com',
        'PORT': '5432',
    },
    'logging_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'logging_db',
        'USER': 'logging_user',
        'PASSWORD': 'password',
        'HOST': 'logging.db.server.com',
        'PORT': '5432',
    }
}

# Required router configuration:
# DATABASE_ROUTERS = ['quiz_project.db_routers.AppBasedRouter']
# APP_DB_ROUTING = {
#     'quiz_api': 'default',
#     'analytics': 'analytics_db',
#     'logging': 'logging_db',
# }


# ============================================================================
# Example 5: Hybrid Setup (App-based + Read/Write Splitting)
# ============================================================================
# Use with: HybridRouter
# Benefits: Combines app separation with read/write splitting

DATABASES_HYBRID = {
    # Main application databases
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'quiz-primary.db.server.com',
        'PORT': '5432',
    },
    'default_replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user_readonly',
        'PASSWORD': 'password',
        'HOST': 'quiz-replica.db.server.com',
        'PORT': '5432',
    },
    # Analytics databases
    'analytics_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics_db',
        'USER': 'analytics_user',
        'PASSWORD': 'password',
        'HOST': 'analytics-primary.db.server.com',
        'PORT': '5432',
    },
    'analytics_replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics_db',
        'USER': 'analytics_user_readonly',
        'PASSWORD': 'password',
        'HOST': 'analytics-replica.db.server.com',
        'PORT': '5432',
    }
}

# Required router configuration:
# DATABASE_ROUTERS = ['quiz_project.db_routers.HybridRouter']
# HYBRID_DB_ROUTING = {
#     'quiz_api': {'primary': 'default', 'replica': 'default_replica'},
#     'analytics': {'primary': 'analytics_db', 'replica': 'analytics_replica'},
# }


# ============================================================================
# Example 6: Multi-Tenant with Separate Databases
# ============================================================================
# Use with: Custom router based on tenant
# Benefits: Complete data isolation per tenant

DATABASES_MULTI_TENANT = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shared_db',  # Shared tables like User, etc.
        'USER': 'shared_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'tenant_1': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tenant_1_db',
        'USER': 'tenant_user',
        'PASSWORD': 'password',
        'HOST': 'tenant1.db.server.com',
        'PORT': '5432',
    },
    'tenant_2': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tenant_2_db',
        'USER': 'tenant_user',
        'PASSWORD': 'password',
        'HOST': 'tenant2.db.server.com',
        'PORT': '5432',
    }
}


# ============================================================================
# Example 7: Different Database Engines
# ============================================================================
# Mix PostgreSQL for main data, MongoDB for logs, Redis for cache

DATABASES_MIXED_ENGINES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'mysql_legacy': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'legacy_db',
        'USER': 'legacy_user',
        'PASSWORD': 'password',
        'HOST': 'legacy.db.server.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
    'sqlite_cache': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/cache.db',
    }
}


# ============================================================================
# Example 8: AWS RDS with Read Replicas
# ============================================================================
DATABASES_AWS_RDS = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'quiz-db.123456.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',  # Use SSL for RDS
        },
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'quiz-db-replica.123456.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',
        },
    }
}


# ============================================================================
# Example 9: Connection Pooling with PgBouncer
# ============================================================================
DATABASES_PGBOUNCER = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'pgbouncer.server.com',  # PgBouncer host
        'PORT': '6432',  # Default PgBouncer port
        'CONN_MAX_AGE': 0,  # Disable Django connection pooling (PgBouncer handles it)
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}


# ============================================================================
# Testing Configuration
# ============================================================================
# For testing, Django automatically creates test databases
# You can control test database behavior:

DATABASES_TEST_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_quiz_db',  # Custom test database name
            'CHARSET': 'utf8',
            'COLLATION': None,
            'MIRROR': None,  # Mirror another database for testing
        }
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quiz_db_replica',
        'USER': 'quiz_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'MIRROR': 'default',  # Use same test database as 'default'
        }
    }
}


# ============================================================================
# Environment-based Configuration Helper
# ============================================================================
def get_database_config(env='development'):
    """
    Helper function to get database configuration based on environment.

    Usage in settings:
        from .db_examples import get_database_config
        DATABASES = get_database_config(os.getenv('DJANGO_ENV', 'development'))
    """
    configs = {
        'development': DATABASES_SINGLE,
        'staging': DATABASES_PRIMARY_REPLICA,
        'production': DATABASES_HYBRID,
    }
    return configs.get(env, DATABASES_SINGLE)
