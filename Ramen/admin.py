from django.contrib import admin
from .models import MyModel, OrderStatus  # OrderStatus 모델도 함께 불러옵니다

class MyModelAdmin(admin.ModelAdmin):
    search_fields = ['date']

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'remaining_count', 'status', 'created_at', 'updated_at']
    search_fields = ['employee_id', 'status']
    list_filter = ['status', 'created_at']  # 필터 추가 (예: status, created_at 등)

admin.site.register(MyModel, MyModelAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)  # OrderStatus를 관리자 페이지에 등록
