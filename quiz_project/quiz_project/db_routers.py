"""
Database routers for quiz_project.

This module provides database routing logic for multi-database setups.
Routers control which database a model's queries are directed to.

Common Use Cases:
1. Read/Write splitting - Route reads to replicas, writes to primary
2. App-based routing - Different apps use different databases
3. Model-based routing - Specific models use specific databases
4. Sharding - Distribute data across multiple databases

For more information, see:
https://docs.djangoproject.com/en/4.2/topics/db/multi-db/
"""


class PrimaryReplicaRouter:
    """
    Router for implementing read/write splitting.

    - All writes go to 'default' (primary database)
    - All reads go to 'replica' database (if available, otherwise default)

    Usage:
    Add to settings: DATABASE_ROUTERS = ['quiz_project.db_routers.PrimaryReplicaRouter']

    Configure databases in settings:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'quiz_db',
            'HOST': 'primary.db.server',
            ...
        },
        'replica': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'quiz_db',
            'HOST': 'replica.db.server',
            ...
        }
    }
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read from replica database.
        Falls back to default if replica doesn't exist.
        """
        return 'replica'

    def db_for_write(self, model, **hints):
        """
        All writes go to the primary (default) database.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in the same database.
        """
        db_set = {'default', 'replica'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations only run on the primary database.
        """
        return db == 'default'


class AppBasedRouter:
    """
    Router that directs database operations based on the app.

    This allows different Django apps to use different databases.

    Usage:
    Add to settings: DATABASE_ROUTERS = ['quiz_project.db_routers.AppBasedRouter']

    Configure app_db_routing in settings:
    APP_DB_ROUTING = {
        'quiz_api': 'default',
        'analytics': 'analytics_db',
        'logs': 'logging_db',
    }

    Configure databases accordingly:
    DATABASES = {
        'default': {...},
        'analytics_db': {...},
        'logging_db': {...},
    }
    """

    def _get_app_db(self, app_label):
        """
        Get the database for a given app from settings.
        """
        from django.conf import settings
        app_db_routing = getattr(settings, 'APP_DB_ROUTING', {})
        return app_db_routing.get(app_label, 'default')

    def db_for_read(self, model, **hints):
        """
        Direct reads to the database configured for the model's app.
        """
        return self._get_app_db(model._meta.app_label)

    def db_for_write(self, model, **hints):
        """
        Direct writes to the database configured for the model's app.
        """
        return self._get_app_db(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same app (same database).
        """
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations run on the correct database for each app.
        """
        return db == self._get_app_db(app_label)


class ModelBasedRouter:
    """
    Router that directs database operations based on specific models.

    This allows fine-grained control over which models use which databases.

    Usage:
    Add to settings: DATABASE_ROUTERS = ['quiz_project.db_routers.ModelBasedRouter']

    Configure model_db_routing in settings:
    MODEL_DB_ROUTING = {
        'quiz_api.UserActivity': 'analytics_db',
        'quiz_api.AuditLog': 'logging_db',
        'auth.User': 'default',
        # Default for all other models
        '_default': 'default',
    }
    """

    def _get_model_db(self, model):
        """
        Get the database for a specific model from settings.
        """
        from django.conf import settings
        model_db_routing = getattr(settings, 'MODEL_DB_ROUTING', {})

        # Check for specific model routing
        model_key = f"{model._meta.app_label}.{model._meta.model_name}"
        if model_key in model_db_routing:
            return model_db_routing[model_key]

        # Fall back to default
        return model_db_routing.get('_default', 'default')

    def db_for_read(self, model, **hints):
        """
        Direct reads to the database configured for the specific model.
        """
        return self._get_model_db(model)

    def db_for_write(self, model, **hints):
        """
        Direct writes to the database configured for the specific model.
        """
        return self._get_model_db(model)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects use the same database.
        """
        db1 = self._get_model_db(obj1.__class__)
        db2 = self._get_model_db(obj2.__class__)
        if db1 == db2:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations run on the correct database for each model.
        """
        if model_name:
            from django.apps import apps
            try:
                model = apps.get_model(app_label, model_name)
                return db == self._get_model_db(model)
            except LookupError:
                pass
        return None


class HybridRouter:
    """
    Hybrid router combining read/write splitting with app-based routing.

    This router:
    1. Routes apps to their designated databases
    2. Within each database group, uses read replicas for reads

    Usage:
    Add to settings: DATABASE_ROUTERS = ['quiz_project.db_routers.HybridRouter']

    Configure hybrid routing in settings:
    HYBRID_DB_ROUTING = {
        'quiz_api': {'primary': 'default', 'replica': 'default_replica'},
        'analytics': {'primary': 'analytics_db', 'replica': 'analytics_replica'},
    }
    """

    def _get_db_config(self, app_label):
        """
        Get the database configuration for an app.
        Returns a dict with 'primary' and 'replica' keys.
        """
        from django.conf import settings
        hybrid_routing = getattr(settings, 'HYBRID_DB_ROUTING', {})

        if app_label in hybrid_routing:
            return hybrid_routing[app_label]

        # Default configuration
        return {'primary': 'default', 'replica': 'default'}

    def db_for_read(self, model, **hints):
        """
        Direct reads to the replica database for the model's app.
        """
        config = self._get_db_config(model._meta.app_label)
        return config.get('replica', config.get('primary', 'default'))

    def db_for_write(self, model, **hints):
        """
        Direct writes to the primary database for the model's app.
        """
        config = self._get_db_config(model._meta.app_label)
        return config.get('primary', 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects belong to the same database group.
        """
        config1 = self._get_db_config(obj1._meta.app_label)
        config2 = self._get_db_config(obj2._meta.app_label)

        if config1.get('primary') == config2.get('primary'):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations run on the primary database for each app.
        """
        config = self._get_db_config(app_label)
        return db == config.get('primary', 'default')
