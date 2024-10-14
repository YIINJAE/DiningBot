"""
ASGI config for config project.

이 파일은 Django 프로젝트의 ASGI 설정 파일입니다.
ASGI(Application Server Gateway Interface)는 Django 애플리케이션이 비동기 서버와 통신할 수 있도록 하는 표준입니다.

ASGI callable을 모듈 수준 변수인 `application`으로 노출합니다.

이 파일에 대한 자세한 내용은 다음 문서에서 확인할 수 있습니다:
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os  # 운영 체제 관련 기능을 제공하는 표준 라이브러리 모듈

# Django의 ASGI 애플리케이션을 가져오는 함수
from django.core.asgi import get_asgi_application

# Django 설정 모듈을 지정
# 'config.settings'는 이 프로젝트에서 사용되는 설정 파일을 가리킵니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ASGI 애플리케이션 객체를 생성하여 `application` 변수에 할당
# 이 객체는 ASGI 서버가 요청을 처리할 때 호출되는 엔트리 포인트입니다.
application = get_asgi_application()
