import os
from celery import Celery

# Define o settings do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Só importa Django depois do settings estar carregado
import django
django.setup()

app = Celery("config")

# Usa configurações do Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Procura tarefas nas apps
app.autodiscover_tasks(related_name="celery_tasks")
