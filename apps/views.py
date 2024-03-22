import requests
import datetime
import time
from django.conf import settings
from django.shortcuts import render,redirect
from proxmoxer import ProxmoxAPI
from django.http import HttpResponse, JsonResponse
from .utils import traffic_format, get_latest_data
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from .models import User, Uservm
from .forms import CustomUserCreationForm
def index(request):
    return HttpResponse("Hello, world. You're at the index page.")

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    user = request.user
    user_vm = Uservm.objects.filter(user_id=user.id)
    print(f"{user} {user_vm}")
    return render(request, 'home.html', {'user_vm': user_vm,  "user": user,})


def manage_vm(request):
    user = request.user
    vm_id = request.POST.get("vm_id", "")
    action = request.POST.get("action", "")
    try:
        user_vm = Uservm.objects.get(vm_id=vm_id)
        if user_vm.manage_vm(action):
            time.sleep(3)
            return redirect(f'/vm_status/{vm_id}')
        else:
            user_vm = Uservm.objects.filter(user_id=user.id)
            return render(request, 'home.html', {'user_vm': user_vm,  "user": user,})
    except Uservm.DoesNotExist:
        user_vm = Uservm.objects.filter(user_id=user.id)
        return render(request, 'home.html', {'user_vm': user_vm,  "user": user,})


def vm_status(request,vm_id):
    vm_status = get_latest_data(vm_id)
    user = request.user
    try:
        user_vm = Uservm.objects.get(vm_id=vm_id)
        user_vm.check_user_permission(user.id)
        return render(request, 'vm_status.html', {'vm_status': vm_status,  "user": user,})
    except Uservm.DoesNotExist:
        user_vm = Uservm.objects.filter(user_id=user.id)
        return render(request, 'home.html', {'user_vm': user_vm,  "user": user,})


def update_data(request):
    vmid = request.GET.get('vmid', None)
    vm_status = get_latest_data(vmid) 
    return JsonResponse(vm_status)