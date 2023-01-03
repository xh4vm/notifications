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
