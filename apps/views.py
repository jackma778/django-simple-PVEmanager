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
from .models import User, UserVPS
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
    user_vps = UserVPS.objects.filter(user_id=user.id)
    return render(request, 'home.html', {'user_vps': user_vps,  "user": user,})


def start_vps(request):
    proxmox = ProxmoxAPI(settings.YOUR_PVE_SERVER, user=settings.YOUR_PVE_USER, password=settings.YOUR_PVE_PASS, verify_ssl=False)
    vm_id = request.POST.get("vm_id", "")
    proxmox.nodes("pve").lxc(vm_id).status.start.post()
    time.sleep(3)
    return redirect(f'/vps_status/{vm_id}')


def stop_vps(request):
    proxmox = ProxmoxAPI(settings.YOUR_PVE_SERVER, user=settings.YOUR_PVE_USER, password=settings.YOUR_PVE_PASS, verify_ssl=False)
    vm_id = request.POST.get("vm_id", "")
    proxmox.nodes("pve").lxc(vm_id).status.stop.post()
    time.sleep(3)
    return redirect(f'/vps_status/{vm_id}')

def vps_status(request,vm_id):
    vps_status = get_latest_data(vm_id)
    user = request.user
    return render(request, 'vps_status.html', {'vps_status': vps_status,  "user": user,})


def update_data(request):
    vmid = request.GET.get('vmid', None)
    vps_status = get_latest_data(vmid) 
    return JsonResponse(vps_status)