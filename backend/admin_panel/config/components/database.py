# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('NOTICE_DB_NAME'),
        'USER': environ.get('NOTICE_DB_USER'),
        'PASSWORD': environ.get('NOTICE_DB_PASSWORD'),
        'HOST': environ.get('NOTICE_DB_HOST', '127.0.0.1'),
        'PORT': environ.get('NOTICE_DB_PORT', 5432),
        'OPTIONS': {
           'options': '-c search_path=public,content'
        }
    }
}

KEY_VALUE_DB_SETTINGS = {
    'host': environ.get('REDIS_HOST', '127.0.0.1'),
    'port': environ.get('REDIS_PORT', 6379),
    'db': environ.get('REDIS_DB', 1),
    'charset': 'utf-8',
    'decode_responses': True
}
