from django.urls import path
from django.contrib.auth import views as auth_views  # Django의 기본 인증 관련 뷰를 불러옴
from . import views  # 같은 앱 내의 views.py에서 정의된 뷰를 가져옴

# 이 앱의 이름을 'common'으로 설정하여 다른 앱들과 구분 가능하게 함
app_name = 'common'

# URL 패턴 정의
urlpatterns = [
    # 로그인 페이지로 연결되는 URL 패턴
    # Django의 기본 `LoginView`를 사용하며, `common/login.html` 템플릿을 지정함
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # 로그아웃 요청을 처리하는 URL 패턴
    # Django의 기본 `LogoutView`를 사용
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 비밀번호 변경 페이지로 연결되는 URL 패턴
    # `views.py`에서 정의한 `change_password` 뷰를 사용
    path('change_password/', views.change_password, name='change_password'),
]
