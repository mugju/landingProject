from .base import *

# same site 문제
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = 'None'
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'None'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEBUG = True
ALLOWED_HOSTS = []