import os

# FORCE_SCRIPT_NAME = "/crm"
# LOGIN_URL = "/crm/login/"
# LOGIN_REDIRECT_URL = "/crm/"
# LOGOUT_REDIRECT_URL = "/crm/"
# STATIC_URL = "/crm-static/"
# MEDIA_ROOT = "/usr/local/makerspaceleiden-crm/var/media"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": "/etc/gandalf/db.cnf",
        },
    }
}

import sys

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "log_to_stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/gandalf-debug.log",
            "maxBytes": 1024 * 1024,
            "backupCount": 10,
            "formatter": "standard",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "propagate": True,
        },
        "django.server": {
            "handlers": ["file"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file"],
            "propagate": True,
        },
        "django.security": {
            "handlers": ["file"],
            "propagate": True,
        },
        "django.db": {
            "handlers": ["file"],
            "propagate": True,
        },
        "django.template": {
            "handlers": ["file"],
            "propagate": True,
        },
        "commands": {
            "handlers": ["log_to_stdout"],
            "level": "DEBUG",
            "propagate": True,
        },
        "": {
            "handlers": ["file"],
            "propagate": True,
        },
    },
}
