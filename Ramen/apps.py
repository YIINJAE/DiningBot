# Ramen/apps.py
from django.apps import AppConfig

class RamenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ramen'

    def ready(self):
        from .modbus_task import start_modbus_thread
        start_modbus_thread()  # Django 앱이 시작될 때 Modbus 스레드 실행
