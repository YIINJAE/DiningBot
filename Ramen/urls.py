from django.urls import path
from .views import index_views, index_3_voice_oder

from django.urls import path




app_name = 'Ramen'

urlpatterns = [

    path('', index_views.index, name='index'), # 제일 초기 화면
    path('index02/', index_views.oder_select, name='index02'), # 일반주문 / 음성주문 선택화면
    #
    path('index04/', index_views.manual_oder, name='index04'), # 일반주문 화면
    path('index03/', index_3_voice_oder.voice_oder, name='index03'), # 음성인식 주문화면

]