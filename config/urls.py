"""
config URL Configuration

이 파일은 Django 프로젝트의 URL 라우팅을 설정합니다.
`urlpatterns`는 URL 경로와 그에 대응하는 뷰를 매핑하는 리스트입니다.
"""

from django.contrib import admin  # 관리자 페이지를 위한 admin 모듈
from django.urls import path, include  # URL 경로 처리를 위한 모듈
from Ramen.views import index_views, index_0_cspower_on  # Ramen 애플리케이션의 뷰를 임포트
from django.conf.urls.static import static  # 정적 파일 서빙을 위한 함수
from django.conf import settings  # 설정을 불러오기 위한 모듈

urlpatterns = [
    # 'init/' 경로가 호출될 때 index_0_cspower_on.cs_poweron 뷰가 실행됨 (로봇 초기화)
    path('init/', index_0_cspower_on.cs_poweron, name='init'),

    # 관리자 페이지의 URL 경로
    path('admin/', admin.site.urls),

    # 'Ramen/' 경로로 시작하는 모든 요청을 Ramen 애플리케이션의 URL 설정으로 위임
    path('Ramen/', include('Ramen.urls')),
    # path('ramen/', include('Ramen.urls')),

    # 'common/' 경로로 시작하는 모든 요청을 common 애플리케이션의 URL 설정으로 위임
    path('common/', include('common.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
# 정적 파일 처리를 위한 경로 설정 (STATIC_URL과 STATIC_ROOT를 기반으로 정적 파일을 서빙)

# 404 에러 페이지가 발생할 때 'common.views.page_not_found' 뷰를 실행하도록 설정
handler404 = 'common.views.page_not_found'
