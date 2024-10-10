import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Import users from a CSV file'  # 명령어에 대한 설명. 'help' 옵션은 커맨드에 대한 도움말 메시지를 제공.

    def add_arguments(self, parser):
        # 이 함수는 명령어에 필요한 인자를 정의합니다.
        # 'csv_file' 인자를 통해 사용자가 CSV 파일의 경로를 입력할 수 있게 합니다.
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing users')

    def handle(self, *args, **options):
        # 이 함수는 명령어가 실행될 때 호출됩니다.
        # 'csv_file' 옵션을 받아서 파일 경로를 가져옵니다.
        csv_file = options['csv_file']
        
        try:
            # CSV 파일을 열어서 읽습니다.
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                # CSV 파일의 각 행을 딕셔너리 형태로 읽어들입니다. 각 열은 헤더 이름으로 참조됩니다.
                reader = csv.DictReader(csvfile)
                
                # CSV 파일의 각 행에 대해 반복합니다.
                for row in reader:
                    employee_id = row['employee_id']  # 'employee_id' 열에서 사번을 가져옴
                    password = row['password']  # 'password' 열에서 비밀번호를 가져옴
                    name = row['name']  # 'name' 열에서 이름을 가져옴

                    # 사용자가 이미 존재하는지 확인합니다.
                    if not User.objects.filter(username=employee_id).exists():
                        # 존재하지 않으면 새 사용자 생성.
                        User.objects.create(
                            username=employee_id,  # 사번을 username으로 사용
                            password=make_password(password),  # 비밀번호는 해싱하여 저장
                            first_name=name  # 이름은 first_name 필드에 저장
                        )
                        # 성공 메시지를 콘솔에 출력.
                        self.stdout.write(self.style.SUCCESS(f"User {employee_id} created with name {name}"))
                    else:
                        # 이미 사용자가 존재하는 경우 경고 메시지를 출력.
                        self.stdout.write(self.style.WARNING(f"User {employee_id} already exists"))
        except FileNotFoundError:
            # 파일을 찾을 수 없는 경우 에러 메시지를 출력.
            self.stdout.write(self.style.ERROR(f"File {csv_file} not found"))
        except Exception as e:
            # 다른 예외가 발생한 경우 에러 메시지를 출력.
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
