### This file is used with channels, disabled for this project
"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WAD2_Project.settings")

django.setup()
application = get_default_application()