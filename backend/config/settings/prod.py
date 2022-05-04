from .base import *

# same site 문제
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

DEBUG = False
ALLOWED_HOSTS = ["3.36.26.172","3.34.144.222","localhost"]