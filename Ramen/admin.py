from django.contrib import admin
from .models import MyModel, OrderStatus  # MyModel과 OrderStatus 모델을 불러옵니다

# MyModel을 위한 관리자 설정
class MyModelAdmin(admin.ModelAdmin):
    search_fields = ['date']  # 관리자 페이지에서 'date' 필드를 검색할 수 있도록 설정

# OrderStatus를 위한 관리자 설정
class OrderStatusAdmin(admin.ModelAdmin):
    # list_display: 관리자 페이지에서 OrderStatus 모델의 리스트 화면에 표시할 필드들
    list_display = ['employee_id', 'remaining_count', 'status', 'created_at', 'updated_at']
    
    # search_fields: 관리자 페이지에서 검색할 수 있는 필드들 (여기서는 employee_id와 status로 검색 가능)
    search_fields = ['employee_id', 'status']
    
    # list_filter: 관리자가 특정 필드별로 데이터를 필터링할 수 있도록 설정
    list_filter = ['status', 'created_at']  # 상태(status)와 생성 날짜(created_at)로 필터링 가능

# MyModel과 MyModelAdmin 설정을 관리자 페이지에 등록
admin.site.register(MyModel, MyModelAdmin)

# OrderStatus와 OrderStatusAdmin 설정을 관리자 페이지에 등록
admin.site.register(OrderStatus, OrderStatusAdmin)
