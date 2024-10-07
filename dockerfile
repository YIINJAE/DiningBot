# Python 베이스 이미지 사용
FROM python:3.9

# 시스템 종속성 설치
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 로그 디렉토리 생성
RUN mkdir -p /app/logs

# 필요한 패키지 설치를 위해 requirements.txt 복사
COPY requirements.txt .

# pip 최신 버전으로 업그레이드
RUN pip install --upgrade pip

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 백업 스크립트를 Docker 이미지에 복사
COPY backup_script.py /app/backup_script.py

# 포트 설정
EXPOSE 8000

# 서버 실행 및 백업 스크립트 실행
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python backup_script.py"]
