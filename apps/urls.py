from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('vps_status/<str:vm_id>/', views.vps_status, name='vps_status'),
    path('update_data/', views.update_data, name='update_data'),
    path('start_vps/', views.start_vps, name='start_vps'),
    path('stop_vps/', views.stop_vps, name='stop_vps'),
]
