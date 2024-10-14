from django.db import models
from datetime import datetime

# MyModel: 주문과 관련된 기본 정보를 저장하는 모델
class MyModel(models.Model):
    date = models.DateTimeField()  # 주문 날짜 및 시간을 저장하는 필드
    employee_id = models.CharField(max_length=100)  # 사원 번호를 저장하는 필드
    name = models.CharField(max_length=200)  # 사원 이름을 저장하는 필드
    count = models.IntegerField()  # 주문한 수량을 저장하는 필드

    def save(self, *args, **kwargs):
        # 주문 날짜가 없을 경우, 현재 시간을 초 단위까지만 저장 (마이크로초 제거)
        if not self.date:
            self.date = datetime.now().replace(microsecond=0)
        super().save(*args, **kwargs)

    # 객체를 문자열로 표현할 때 사용 (관리자 페이지 등에서 보기 편하게)
    def __str__(self):
        # 주문의 날짜, 사원 번호, 사원 이름, 주문 수량을 문자열로 반환
        return f'{self.date} - {self.employee_id} - {self.name} - {self.count}'

# OrderStatus: 주문의 상태와 관련된 정보를 저장하는 모델
class OrderStatus(models.Model):
    employee_id = models.CharField(max_length=100)  # 사원 번호 (ID)
    name = models.CharField(max_length=200)  # 사원 이름
    initial_count = models.IntegerField(default=0)  # 최초 주문 수량 (주문을 시작할 때 수량)
    remaining_count = models.IntegerField(default=0)  # 남은 주문 수량 (남아있는 수량)
    
    # 주문 상태 필드 ('PREPARING'은 준비 중, 'COMPLETED'는 완료됨)
    status = models.CharField(max_length=20, default='PREPARING', choices=[
        ('PREPARING', '준비 중'),
        ('COMPLETED', '완료됨'),
    ])  

    created_at = models.DateTimeField()  # 주문이 처음 생성된 시간
    updated_at = models.DateTimeField()  # 주문이 마지막으로 수정된 시간

    def save(self, *args, **kwargs):
        # 생성 시간(created_at)이 없을 경우, 현재 시간을 초 단위까지만 저장
        if not self.created_at:
            self.created_at = datetime.now().replace(microsecond=0)
        
        # 매번 저장 시 갱신된 시간을 초 단위까지만 저장
        self.updated_at = datetime.now().replace(microsecond=0)
        
        # 부모 클래스의 save() 메서드를 호출하여 실제 DB 저장을 처리
        super().save(*args, **kwargs)

    def update_count(self, decrement):
        """
        하드웨어에 의해 남은 주문 수량을 감소시키는 함수.
        주문의 남은 수량을 감소시키고, 만약 0 이하가 되면 상태를 완료로 변경.
        """
        # 남은 주문 수량에서 주어진 감소 값을 빼줌
        self.remaining_count -= decrement
        
        # 남은 주문 수량이 0 이하로 떨어지면 0으로 고정하고, 상태를 '완료됨'으로 변경
        if self.remaining_count <= 0:
            self.remaining_count = 0  # 수량이 음수로 내려가지 않도록 0으로 설정
            self.status = 'COMPLETED'  # 주문 상태를 '완료됨'으로 변경
        
        # 변경된 사항을 DB에 저장
        self.save()

    # 객체를 문자열로 표현할 때 사용 (관리자 페이지 등에서 보기 편하게)
    def __str__(self):
        # 사원 번호, 이름, 남은 수량을 문자열로 반환
        return f'{self.employee_id} - {self.name} - 남은 수량: {self.remaining_count}'
