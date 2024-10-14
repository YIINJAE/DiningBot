"""
Django settings for config project.

이 파일은 Django 프로젝트의 기본 설정을 정의합니다.
이 설정은 프로젝트의 다양한 옵션을 구성하는 데 사용됩니다.
"""

from pathlib import Path  # 경로 관련 모듈

# 프로젝트 내에서 경로를 쉽게 처리하기 위한 BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent


# 빠른 개발 환경 설정
# 운영 환경에서는 적합하지 않으며, 이를 위한 추가 설정이 필요함
# https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# 보안 키 (운영 환경에서는 외부에 노출되지 않도록 비밀로 관리)
SECRET_KEY = 'django-insecure-*zx=+ba8-02np&+#3p%^#9_k6k@4urtg(lyhjl)+cqdxf=%93s'

# 운영 환경에서는 DEBUG를 False로 설정하여 보안을 강화
DEBUG = True

# 허용할 호스트 목록 (운영 환경에서 사용될 IP 주소 또는 도메인)
ALLOWED_HOSTS = ['192.168.1.210', 'localhost', '127.0.0.1']


# 애플리케이션 정의

INSTALLED_APPS = [
    'django.contrib.admin',  # 관리자 인터페이스
    'django.contrib.auth',  # 인증 시스템
    'django.contrib.contenttypes',  # 컨텐츠 타입
    'django.contrib.sessions',  # 세션 관리
    'django.contrib.messages',  # 메시지 프레임워크
    'django.contrib.staticfiles',  # 정적 파일 관리
    # 추가 애플리케이션
    'Ramen.apps.RamenConfig',  # Ramen 애플리케이션
    'common.apps.CommonConfig',  # 공통 기능 애플리케이션
]

# 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 보안 관련 미들웨어
    'django.contrib.sessions.middleware.SessionMiddleware',  # 세션 관리 미들웨어
    'django.middleware.common.CommonMiddleware',  # 공통 미들웨어
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 보호 미들웨어
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 인증 관리 미들웨어
    'django.contrib.messages.middleware.MessageMiddleware',  # 메시지 관리 미들웨어
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking 보호 미들웨어
]

# 프로젝트의 URL 패턴 설정
ROOT_URLCONF = 'config.urls'

# 템플릿 엔진 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Django 템플릿 엔진 사용
        'DIRS': [BASE_DIR / 'Templates'],  # 템플릿 파일들이 위치하는 경로
        'APP_DIRS': True,  # 애플리케이션 내의 템플릿 디렉토리 자동 검색
        'OPTIONS': {
            'context_processors': [  # 템플릿 렌더링 시 기본적으로 사용될 컨텍스트 처리기
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 설정 (운영 환경에서 사용)
WSGI_APPLICATION = 'config.wsgi.application'


# 데이터베이스 설정 (SQLite 사용)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite3 엔진 사용
        'NAME': BASE_DIR / 'db.sqlite3',  # 데이터베이스 파일 경로
    }
}


# 비밀번호 검증기 설정 (비밀번호의 보안 기준을 정의)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 국제화 및 지역화 설정
# 기본 언어 및 시간대 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

# 지역화 기능 활성화
USE_I18N = True

# 타임존 정보를 사용하지 않도록 설정
USE_TZ = False


# 정적 파일 설정 (CSS, JS, 이미지 파일 경로)
STATIC_URL = '/static/'

# 정적 파일 디렉토리 추가
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 기본 자동 필드 타입 설정 (기본적으로 BigAutoField 사용)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 로그 파일 경로 설정
LOG_DIR = BASE_DIR / 'logs'

# 로그 디렉토리 생성 확인 (없으면 생성)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)


import os
import sys
import logging

# 로깅 설정
LOGGING = {
    'version': 1,  # 로깅 설정의 버전
    'disable_existing_loggers': False,  # 기존의 로거 비활성화 여부
    'filters': {
        'ignore_order_status': {  # 주문 상태 로그를 제외하는 필터
            '()': 'Ramen.utils.IgnoreOrderStatusFilter',  # 필터의 실제 경로
        },
    },
    'formatters': {
        'verbose': {  # 자세한 로그 출력 형식
            'format': '{asctime} {name} {levelname} {message}',  # 시간, 로거 이름, 레벨, 메시지 출력
            'style': '{',
        },
        'simple': {  # 간단한 로그 출력 형식
            'format': '{asctime} {levelname} {message}',  # 시간, 레벨, 메시지 출력
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',  # 시간 형식 지정
        },
    },
    'handlers': {
        'file': {  # 로그 파일로 기록하는 핸들러
            'level': 'INFO',  # INFO 레벨 이상의 로그만 기록
            'class': 'logging.FileHandler',  # 파일로 로그를 기록하는 클래스 사용
            'filename': LOG_DIR / 'django.log',  # 로그 파일 경로
            'formatter': 'verbose',  # verbose 형식 사용
            'filters': ['ignore_order_status'],  # 주문 상태 로그 필터링 적용
        },
        'console': {  # 콘솔에 로그 출력하는 핸들러
            'level': 'INFO',  # INFO 레벨 이상의 로그만 출력
            'class': 'logging.StreamHandler',  # 콘솔 출력 클래스
            'formatter': 'simple',  # simple 형식 사용
            'stream': sys.stdout,  # 표준 출력으로 로그 출력
        },
    },
    'loggers': {
        'django.server': {  # Django 서버 로그
            'handlers': ['file', 'console'],  # 파일과 콘솔 모두에 출력
            'level': 'INFO',  # INFO 레벨 이상의 로그만 기록
            'filters': ['ignore_order_status'],  # 주문 상태 로그 필터링 적용
            'propagate': False,  # 로그 전파 중단
        },
    },
}
