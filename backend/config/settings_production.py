from .settings_base import *  # noqa: F401,F403

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# S3 default storage in production
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
