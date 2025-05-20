"""
ASGI config for delivery_control project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os, dotenv

from django.core.asgi import get_asgi_application

dotenv.load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_control.settings')

application = get_asgi_application()
