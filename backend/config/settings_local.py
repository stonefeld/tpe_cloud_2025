from .settings_base import *  # noqa: F401,F403

DEBUG = True

# Use SQLite for local development/testing by default
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Local filesystem storage
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# CORS settings for local development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
