from django.contrib import admin
from django.urls import path, include
from Ramen.views import index_views, index_0_cspower_on
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('init/', index_0_cspower_on.cs_poweron, name='init'),
    path('admin/', admin.site.urls),
    path('Ramen/', include('Ramen.urls')),
    path('common/', include('common.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'common.views.page_not_found'