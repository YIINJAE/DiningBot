from django.urls import path
from .views import index_views

from django.urls import path




app_name = 'Ramen'

urlpatterns = [

    path('', index_views.index, name='index'), # 제일 초기 화면

]