import os
import sys	
sys.path.append('/var/www/')
sys.path.append('/var/www/ctfmanager/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ctfmanager.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
