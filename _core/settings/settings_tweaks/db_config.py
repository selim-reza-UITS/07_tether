from _core.settings.base import BASE_DIR

LOCAL_SQLITE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

LOCAL_POSTGRESQL_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'masteruser',
        'PASSWORD': '12345678',
        'HOST': 'w3-django-project.cdxmgq9zqqlr.us-east-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}


PRODUCTION_POSTGRESQL_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'masteruser',
        'PASSWORD': '12345678',
        'HOST': 'w3-django-project.cdxmgq9zqqlr.us-east-1.rds.amazonaws.com',
        'PORT': '5432'
    }
}