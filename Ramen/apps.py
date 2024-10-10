# Ramen/apps.py
from django.apps import AppConfig  # Django의 앱 설정을 관리하는 AppConfig 클래스를 불러옵니다

# Ramen 앱의 설정을 정의하는 클래스
class RamenConfig(AppConfig):
    # Django 모델에서 기본적으로 사용될 기본 필드 타입을 지정
    default_auto_field = 'django.db.models.BigAutoField'  # 기본적으로 'BigAutoField'를 자동 생성 필드로 사용하도록 설정
    name = 'Ramen'  # 이 앱의 이름을 'Ramen'으로 지정

    # 앱이 준비될 때 실행되는 메소드 (앱 시작 시 특정 초기화 작업 수행 가능)
    def ready(self):
        from .modbus_task import start_modbus_thread  # modbus_task.py에서 start_modbus_thread 함수를 불러옵니다
        start_modbus_thread()  # Django 앱이 시작될 때 Modbus 스레드를 실행하여 통신 작업을 시작
