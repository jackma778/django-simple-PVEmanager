from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('vm_status/<str:vm_id>/', views.vm_status, name='vm_status'),
    path('update_data/', views.update_data, name='update_data'),
    path('manage_vm/', views.manage_vm, name='manage_vm'),
]
