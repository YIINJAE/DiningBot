from django.db import connection  # Django의 데이터베이스 연결을 관리하는 모듈을 임포트

# 데이터베이스 무결성을 확인하는 함수
def check_database_integrity():
    # 데이터베이스에 직접 SQL 쿼리를 실행하기 위해 커서를 사용
    with connection.cursor() as cursor:
        # SQLite의 무결성 검사 쿼리를 실행
        cursor.execute('PRAGMA integrity_check;')
        
        # 무결성 검사 결과의 첫 번째 행을 가져옴
        result = cursor.fetchone()
        
        # 결과를 출력 (무결성 문제 시 에러 메시지 또는 'ok' 출력)
        print(result)

# 무결성 검사 함수를 실행
check_database_integrity()
