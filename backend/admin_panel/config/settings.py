"""Django settings for config project."""

from os import environ
from pathlib import Path

from config.components.constants import URL_SCHEME
from dotenv import load_dotenv
from split_settings.tools import include

# Build paths inside the project.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent.parent
load_dotenv(Path(ROOT_DIR, '.env'))

include(
    'components/database.py',
    'components/constants.py'
)


SECRET_KEY = environ.get('SECRET_KEY')

DEBUG = environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')

if DEBUG:
    INTERNAL_IPS = environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',

    'notice.apps.NoticeConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CELERY
# amqp://user:pass@host:5672/vhost
CELERY_BROKER_URL = '{0}{1}:{2}@{3}:{4}{5}'.format(
    environ.get('CELERY_BROKER_NAME', 'pyamqp://'),
    environ.get('RABBITMQ_DEFAULT_USER', None),
    environ.get('RABBITMQ_DEFAULT_PASS', None),
    environ.get('RABBITMQ_HOST', 'localhost'),
    environ.get('RABBITMQ_PORT', 5672),
    environ.get('RABBITMQ_DEFAULT_VHOST', '/'),
)

# CELERY_RESULT_BACKEND = '{0}{1}:{2}@{3}:{4}/{5}'.format(
#     environ.get('CELERY_RESULT_BACKEND', 'db+postgresql://'),
#     environ.get('NOTICE_DB_USER', None),
#     environ.get('NOTICE_DB_PASSWORD', None),
#     environ.get('NOTICE_DB_HOST', 'localhost'),
#     environ.get('NOTICE_DB_PORT', 5432),
#     environ.get('NOTICE_DB_NAME', None),
# )


CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# CELERY_BEAT_SCHEDULE = {
#     'queue_every_five_mins': {
#         'task': 'polls.tasks.query_every_five_mins',
#         'schedule': crontab(minute=5),
#     },
# }

CELERY_DAYS_PERIOD_OF_NEWS = environ.get('CELERY_DAYS_PERIOD_OF_NEWS', 7)

NOTICE_API_ENTRYPOINT = '{0}{1}:{2}{3}/{4}/{5}'.format(
    URL_SCHEME,
    environ.get('PROJECT_NOTICE_API_HOST', 'localhost'),
    environ.get('PROJECT_NOTICE_API_PORT', 8000),
    environ.get('PROJECT_NOTICE_API_PATH', '/api'),
    environ.get('PROJECT_NOTICE_API_VERSION', 'v1'),
    environ.get('NOTICE_API_ENTRYPOINT', 'events'),
)
