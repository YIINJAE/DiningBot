"""
db.backup script
"""

import os
import shutil
import time
from datetime import datetime, timedelta
import schedule

# DB 백업 디렉토리
BACKUP_DIR = "/app/db_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# DB 파일 경로
DB_PATH = "/app/db.sqlite3"

# 백업을 수행하는 함수
def backup_db():
    now = datetime.now()
    backup_filename = f"db_backup_{now.strftime('%Y%m%d_%H%M%S')}.sqlite3"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")

# 오래된 백업 파일 삭제 함수 (7일이 지난 백업 삭제)
def cleanup_old_backups():
    now = datetime.now()
    cutoff = now - timedelta(days=7)
    
    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if file_time < cutoff:
                os.remove(file_path)
                print(f"Deleted old backup: {file_path}")

# 매일 오전 8시에 백업 및 정리 작업을 수행
schedule.every().day.at("09:51").do(backup_db)
schedule.every().day.at("09:51").do(cleanup_old_backups)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)