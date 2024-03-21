from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render,redirect
from proxmoxer import ProxmoxAPI
import requests
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from proxmoxer import ProxmoxAPI
import requests
import datetime



def get_latest_data(vm_id):
    # 连接到 Proxmox VE
    proxmox = ProxmoxAPI(settings.YOUR_PVE_SERVER, user=settings.YOUR_PVE_USER, password=settings.YOUR_PVE_PASS, verify_ssl=False)

    # 获取服务器状态数据
    lxc_status = proxmox.nodes("pve").lxc(vm_id).status.current.get()

    # 处理数据
    cpu_usage = round(lxc_status['cpu'] * 100, 2)
    lxc_status['cpu'] = cpu_usage

    mem_usage = lxc_status['mem']
    max_mem = lxc_status['maxmem']
    mem_usage_percentage = (mem_usage / max_mem) * 100 if max_mem != 0 else 0
    lxc_status['mem_usage_percentage'] = round(mem_usage_percentage, 2)

    disk_usage = lxc_status['disk']
    max_disk = lxc_status['maxdisk']
    disk_usage_percentage = (disk_usage / max_disk) * 100 if max_disk != 0 else 0
    lxc_status['disk_usage_percentage'] = round(disk_usage_percentage, 2)

    lxc_status['uptime'] = str(datetime.timedelta(seconds=lxc_status['uptime']))
    lxc_status['mem'] = traffic_format(lxc_status['mem'])
    lxc_status['disk'] = traffic_format(lxc_status['disk'])
    lxc_status['maxdisk'] = traffic_format(lxc_status['maxdisk'])
    lxc_status['maxmem'] = traffic_format(lxc_status['maxmem'])
    lxc_status['net'] = traffic_format(lxc_status['netin'] + lxc_status['netout'])
    return lxc_status



def traffic_format(traffic):
    if traffic < 0:
        abs_traffic = abs(traffic)
        if abs_traffic < 1024 * 1024:
            return str(round((traffic / (1024.0 * 1024)), 1)) + "MB"
        elif abs_traffic < 1024 * 1024 * 1024:
            return str(round((traffic / (1024.0 * 1024)), 1)) + "MB"
        else:
            return str(round((traffic / 1073741824.0), 1)) + "GB"
    
    if traffic < 1024 * 8:
        return str(int(traffic)) + "B"

    if traffic < 1024 * 1024:
        return str(round((traffic / 1024.0), 1)) + "KB"

    if traffic < 1024 * 1024 * 1024:
        return str(round((traffic / (1024.0 * 1024)), 1)) + "MB"

    return str(round((traffic / 1073741824.0), 1)) + "GB"