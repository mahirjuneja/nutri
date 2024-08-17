from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Admin_Module.views import get_products_for_company, get_orders_for_company

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_atlantis.urls')),
    path('admin_module/',include('Admin_Module.urls')),
    path('get_products_for_company/', get_products_for_company, name='get_products_for_company'),
    path('get_orders_for_company/', get_orders_for_company, name='get_orders_for_company'),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)