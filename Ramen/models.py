from django.db import models
from datetime import datetime

# MyModel: 주문과 관련된 기본 정보를 저장하는 모델
class MyModel(models.Model):
    date = models.DateTimeField()  # 주문 날짜 및 시간을 저장하는 필드
    employee_id = models.CharField(max_length=100)  # 사원 번호를 저장하는 필드
    name = models.CharField(max_length=200)  # 사원 이름을 저장하는 필드
    count = models.IntegerField()  # 주문한 수량을 저장하는 필드

    def save(self, *args, **kwargs):
        # 주문 날짜가 없을 경우 현재 시간을 초 단위까지만 저장
        if not self.date:
            self.date = datetime.now().replace(microsecond=0)
        super().save(*args, **kwargs)

    # 객체를 문자열로 표현할 때 사용 (관리자 페이지 등에서 보기 편하게)
    def __str__(self):
        return f'{self.date} - {self.employee_id} - {self.name} - {self.count}'

# OrderStatus: 주문의 상태와 관련된 정보를 저장하는 모델
class OrderStatus(models.Model):
    employee_id = models.CharField(max_length=100)  # 사원 번호 (ID)
    name = models.CharField(max_length=200)  # 사원 이름
    initial_count = models.IntegerField(default=0)  # 최초 주문 수량
    remaining_count = models.IntegerField(default=0)  # 남은 주문 수량
    status = models.CharField(max_length=20, default='PREPARING', choices=[
        ('PREPARING', '준비 중'),
        ('COMPLETED', '완료됨'),
    ])  # 주문의 상태 ('준비 중', '완료됨' 중 하나)

    created_at = models.DateTimeField()  # 주문이 생성된 시간
    updated_at = models.DateTimeField()  # 주문이 마지막으로 업데이트된 시간

    def save(self, *args, **kwargs):
        # created_at과 updated_at을 초 단위까지만 저장 (마이크로초 제거)
        if not self.created_at:
            self.created_at = datetime.now().replace(microsecond=0)
        self.updated_at = datetime.now().replace(microsecond=0)
        super().save(*args, **kwargs)

    def update_count(self, decrement):
        """하드웨어에 의해 남은 수량을 감소시키는 함수"""
        self.remaining_count -= decrement  # 남은 주문 수량을 감소
        if self.remaining_count <= 0:  # 남은 수량이 0 이하가 되면
            self.remaining_count = 0  # 남은 수량을 0으로 고정
            self.status = 'COMPLETED'  # 상태를 '완료됨'으로 변경
        self.save()  # 변경된 사항을 저장

    # 객체를 문자열로 표현할 때 사용 (관리자 페이지 등에서 보기 편하게)
    def __str__(self):
        return f'{self.employee_id} - {self.name} - 남은 수량: {self.remaining_count}'
