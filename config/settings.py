import os, json

DEBUG = False

# set base dir path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set language & timezone
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

KEY_PATH = os.path.join(BASE_DIR, 'secret_keys.json')
keys = dict()
with open(KEY_PATH) as f:
    keys = json.loads(f.read())

# set keys & aws s3 bucket
if DEBUG == True:
    SECRET_KEY = 'ksdafja!@#!#asflksjfd^%$%klsnf!@#@#!#'
    JWT_SECRET_KEY = '123fhksjdnnm.nv.@#$@#$vx.!@#!@#sdv@!#'
    AWS_S3_BUCKET = 'lisn'
    AWS_S3_MEDIA_DIR = 'audio-dev1/'
else:
    SECRET_KEY = keys['DJANGO_SECRET_KEY']
    JWT_SECRET_KEY = keys['JWT_SECRET_KEY']
    AWS_S3_BUCKET = 'lisn'
    AWS_S3_MEDIA_DIR = 'audio/'

# set email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = keys['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = keys['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# set cors
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# set url & root
STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'api',
]

if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': keys['DATABASE_NAME'],
            'USER': keys['DATABASE_USER'],
            'PASSWORD': keys['DATABASE_PASSWORD'],
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
            }
        }
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static')
        ],
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
