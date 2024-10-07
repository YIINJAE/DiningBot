# models.py
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

# 새로운 OrderStatus 모델 생성
class OrderStatus(models.Model):
    employee_id = models.CharField(max_length=100)  # 사번
    name = models.CharField(max_length=200)        # 직원 이름
    initial_count = models.IntegerField(default=0) # 초기 주문 수량
    remaining_count = models.IntegerField(default=0) # 남은 주문 수량
    status = models.CharField(max_length=20, default='PREPARING', choices=[
        ('PREPARING', '준비 중'),
        ('COMPLETED', '완료됨'),
    ])  # 주문 상태
    created_at = models.DateTimeField()   # 주문 생성 시간
    updated_at = models.DateTimeField()   # 주문 업데이트 시간

    def save(self, *args, **kwargs):
        # created_at과 updated_at에 현재 시간을 초 단위까지만 저장
        if not self.created_at:
            self.created_at = datetime.now().replace(microsecond=0)
        self.updated_at = datetime.now().replace(microsecond=0)
        
        super().save(*args, **kwargs)

    def update_count(self, decrement):
        """하드웨어 동작에 따른 count 감소 로직"""
        self.remaining_count -= decrement
        if self.remaining_count <= 0:
            self.remaining_count = 0
            self.status = 'COMPLETED'
        self.save()

    def __str__(self):
        return f'{self.employee_id} - {self.name} - 남은 수량: {self.remaining_count}'


# from django.db import models
# from datetime import datetime


# class MyModel(models.Model):
#     date = models.DateTimeField()  # auto_now_add 제거
#     employee_id = models.CharField(max_length=100)
#     name = models.CharField(max_length=200)
#     count = models.IntegerField()

#     def save(self, *args, **kwargs):
#         # 현재 시간을 초 단위까지만 저장
#         if not self.date:
#             self.date = datetime.now().replace(microsecond=0)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.date} - {self.employee_id} - {self.name} - {self.count}'

# class OrderStatus(models.Model):
#     employee_id = models.CharField(max_length=100)  # 사번
#     name = models.CharField(max_length=200)        # 직원 이름
#     initial_count = models.IntegerField(default=0) # 초기 주문 수량
#     remaining_count = models.IntegerField(default=0) # 남은 주문 수량
#     status = models.CharField(max_length=20, default='PREPARING', choices=[
#         ('PREPARING', '준비 중'),
#         ('COMPLETED', '완료됨'),
#     ])  # 주문 상태
#     created_at = models.DateTimeField(auto_now_add=True)   # 주문 생성 시간
#     updated_at = models.DateTimeField(auto_now=True)       # 주문 업데이트 시간

#     def update_count(self, decrement):
#         """하드웨어 동작에 따른 count 감소 로직"""
#         self.remaining_count -= decrement
#         if self.remaining_count <= 0:
#             self.remaining_count = 0
#             self.status = 'COMPLETED'
#         self.save()

#     def __str__(self):
#         return f'{self.employee_id} - {self.name} - 남은 수량: {self.remaining_count}'
