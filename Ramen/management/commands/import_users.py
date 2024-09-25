import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        # CSV 파일 경로를 인자로 받습니다.
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing users')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    employee_id = row['employee_id']
                    password = row['password']
                    name = row['name']  # CSV에서 name 필드를 가져옵니다.

                    if not User.objects.filter(username=employee_id).exists():
                        User.objects.create(
                            username=employee_id,
                            password=make_password(password),
                            first_name=name  # name을 first_name으로 저장합니다.
                        )
                        self.stdout.write(self.style.SUCCESS(f"User {employee_id} created with name {name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"User {employee_id} already exists"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))