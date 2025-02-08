"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .opentelemetry_config import configure_tracing
from opentelemetry.instrumentation.django import DjangoInstrumentor

configure_tracing()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
configure_tracing()
# configure_tracing()

# Instrument Django
DjangoInstrumentor().instrument()
application = get_wsgi_application()
