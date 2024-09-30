from django.urls import path
from .views import index_views, index_5_oder_comp, index_3_voice_oder, index_0_cspower_on, db_index00, chang_pass
from django.urls import path

app_name = 'Ramen'

urlpatterns = [
    path('', index_views.index, name='index'), # 제일 초기 화면
    path('index02/', index_views.oder_select, name='index02'), # 일반주문 / 음성주문 선택화면
    path('index03/', index_3_voice_oder.voice_oder, name='index03'), # 음성인식 주문화면
    path('index04/', index_views.manual_oder, name='index04'), # 일반주문 화면
    path('index05/<int:count>/<str:employee_id>/', index_5_oder_comp.manual_oder_complete, name='index05'), # 일반주문 확인 완료
    path('db_index00/', db_index00.login_view, name='db_index00'),  # 로그인 페이지
    path('pass/<str:employee_id>/<int:count>/', chang_pass.change_password, name='pass'),  # 로그인 페이지
    path('login/', db_index00.login_view, name='login'),
]