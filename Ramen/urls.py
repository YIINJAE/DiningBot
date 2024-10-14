from django.urls import path
from .views import (
    index_views, 
    index_5_oder_comp, 
    index_3_voice_oder, 
    index_0_cspower_on, 
    db_index00, 
    chang_pass, 
    get_oder_remain, 
    order_views
)
from django.urls import path

# Django의 app 네임스페이스를 설정하여 URL 경로들이 충돌하지 않게 처리
app_name = 'Ramen'

# Ramen 애플리케이션의 URL 패턴 정의
urlpatterns = [
    path('', index_views.index, name='index'),  # 앱 초기 화면으로 이동하는 URL 패턴
    path('index02/', index_views.oder_select, name='index02'),  # 일반주문/음성주문 선택 화면으로 이동하는 URL 패턴
    path('index03/', index_3_voice_oder.voice_oder, name='index03'),  # 음성인식 주문 화면으로 이동하는 URL 패턴
    path('index04/', index_views.manual_oder, name='index04'),  # 일반 주문 화면으로 이동하는 URL 패턴
    path('index05/<int:count>/<str:employee_id>/', index_5_oder_comp.manual_oder_complete, name='index05'),  # 주문 완료 화면 (주문 수량과 사번이 포함된 URL 파라미터)
    path('db_index00/', db_index00.login_view, name='db_index00'),  # 로그인 페이지로 이동하는 URL 패턴
    path('pass/<str:employee_id>/<int:count>/', chang_pass.change_password, name='pass'),  # 비밀번호 변경 페이지로 이동하는 URL 패턴 (사번과 주문 수량 파라미터 포함)
    path('order_status/', order_views.order_status_view, name='order_status'),  # 주문 상태 화면으로 이동하는 URL 패턴 (주문 상태 조회)
    path('login/', db_index00.login_view, name='login'),  # 로그인 페이지로 이동하는 URL 패턴 (로그인 화면 접근)
    path('get_active_orders/', order_views.get_active_orders, name='get_active_orders'),  # 주문 상태를 Ajax로 갱신하기 위한 URL 패턴 (Ajax 요청 처리)
]
