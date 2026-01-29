import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmAshiqurzamman_ID_JobPortal.settings')

application = get_asgi_application()
