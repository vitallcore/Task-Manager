import os

import rollbar
from django.conf import settings
from django.core.wsgi import get_wsgi_application

rollbar.init(**settings.ROLLBAR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

application = get_wsgi_application()
