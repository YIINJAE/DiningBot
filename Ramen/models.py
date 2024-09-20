from django.db import models
from datetime import datetime

class MyModel(models.Model):
    date = models.DateTimeField()  # auto_now_add 제거
    employee_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    count = models.IntegerField()

    def save(self, *args, **kwargs):
        # 현재 시간을 초 단위까지만 저장
        if not self.date:
            self.date = datetime.now().replace(microsecond=0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.date} - {self.employee_id} - {self.name} - {self.count}'