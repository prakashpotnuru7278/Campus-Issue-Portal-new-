from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reports import views  
from django.conf import settings

urlpatterns = [
    path('', include('reports.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('dashboard/login/', views.custom_admin_login, name='admin_login'),  
    path('admin/', admin.site.urls),  
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
