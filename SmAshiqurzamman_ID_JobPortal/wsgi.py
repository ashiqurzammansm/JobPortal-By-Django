import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmAshiqurzamman_ID_JobPortal.settings')

application = get_wsgi_application()
