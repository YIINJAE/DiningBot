"""
db.backup script
"""

import os  # 파일 및 디렉토리 경로 관리를 위한 모듈
import shutil  # 파일 복사를 위한 모듈
import time  # 시간 관련 함수 제공 (sleep 등)
from datetime import datetime, timedelta  # 날짜 및 시간 관리
import schedule  # 스케줄링을 위한 라이브러리

# DB 백업을 저장할 디렉토리
BACKUP_DIR = "/app/db_backups"
# 백업 디렉토리가 없으면 생성
os.makedirs(BACKUP_DIR, exist_ok=True)

# 백업할 DB 파일 경로
DB_PATH = "/app/db.sqlite3"

# DB 백업을 수행하는 함수
def backup_db():
    now = datetime.now()  # 현재 시간 가져오기
    # 백업 파일 이름을 현재 날짜와 시간으로 생성
    backup_filename = f"db_backup_{now.strftime('%Y%m%d_%H%M%S')}.sqlite3"
    # 백업 파일의 전체 경로 설정
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # 원본 DB 파일을 백업 경로로 복사
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")  # 백업 완료 메시지 출력

# 7일이 지난 오래된 백업 파일 삭제 함수
def cleanup_old_backups():
    now = datetime.now()  # 현재 시간 가져오기
    cutoff = now - timedelta(days=7)  # 7일 전 시간을 계산
    
    # 백업 디렉토리의 파일들을 순회
    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(file_path):  # 파일인지 확인
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))  # 파일 생성 시간 가져오기
            if file_time < cutoff:  # 파일 생성 시간이 7일 이전이면
                os.remove(file_path)  # 파일 삭제
                print(f"Deleted old backup: {file_path}")  # 삭제 메시지 출력

# 매일 오전 9시 30분에 백업 및 오래된 백업 삭제를 스케줄
schedule.every().day.at("09:30").do(backup_db)  # 백업 작업 스케줄 설정
schedule.every().day.at("09:30").do(cleanup_old_backups)  # 오래된 백업 삭제 작업 스케줄 설정

# 스크립트의 메인 루프
if __name__ == "__main__":
    while True:
        # 스케줄에 따라 작업 실행
        schedule.run_pending()  # 예약된 작업 실행
        time.sleep(60)  # 60초 대기 후 다시 실행
