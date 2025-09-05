"""
Local development settings proxy to `config.settings.local`.

We keep this file for Django's default entry point but immediately import
all settings from the split settings module.
"""

from .settings_local import *  # noqa: F401,F403
