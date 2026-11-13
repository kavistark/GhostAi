"""
PythonAnywhere WSGI Configuration for GHOST (Django Framework)
Path on PythonAnywhere: /var/www/ghostassist_pythonanywhere_com_wsgi.py
Project directory: /home/GhostAssist/GhostAi
"""

import os
import sys

# 1. Add project root to sys.path
path = '/home/GhostAssist/GhostAi'
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'ghost_project.settings'

# 3. Load standard Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
