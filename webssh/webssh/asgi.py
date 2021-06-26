"""
ASGI入口点，运行Django，然后运行在settings.py ASGI_APPLICATION 中定义的应用程序
安装：pip install daphne
运行：daphne -p 8001 webssh.asgi:application
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webssh.settings")
django.setup()
application = get_default_application()