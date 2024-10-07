from django.db import connection

def check_database_integrity():
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA integrity_check;')
        result = cursor.fetchone()
        print(result)

check_database_integrity()
