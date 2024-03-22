from django.contrib.auth.models import AbstractUser
from proxmoxer import ProxmoxAPI
from django.db import models
from django.conf import settings
from django.db import connection, models, transaction
from decimal import Decimal
from .utils import get_time,get_date

class User(AbstractUser):
    balance = models.DecimalField(
        verbose_name="balance",
        decimal_places=2,
        max_digits=10,
        default=0,
        editable=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

class Uservm(models.Model):
    user_id = models.PositiveIntegerField()
    vm_id = models.PositiveIntegerField()
    expire_date = models.DateField("包月到期日", null=True, blank=True, db_index=True)
    cost = models.DecimalField(
        verbose_name="balance",
        decimal_places=2,
        max_digits=10,
        default=0,
        editable=True,
        null=True,
        blank=True,
    )

    def get_vm_status(self):
        proxmox = ProxmoxAPI(settings.YOUR_PVE_SERVER, user=settings.YOUR_PVE_USER, password=settings.YOUR_PVE_PASS, verify_ssl=False)
        vm = proxmox.nodes("pve").lxc(self.vm_id).status.current.get()
        print(f"检查vm状态：{vm}")
        if vm:
            return vm.get('status', '') == 'running'
        else:
            return False

    def check_expire(self):
        if self.expire_date < get_date():
            return True
        else:
            return False

    def check_user_permission(self, user_id):
        if self.user_id != user_id:
            raise PermissionDenied("You don't have permission to access this vm.")

    def manage_vm(self, action):
        print(action)
        try:
            proxmox = ProxmoxAPI(settings.YOUR_PVE_SERVER, user=settings.YOUR_PVE_USER, password=settings.YOUR_PVE_PASS, verify_ssl=False)
            if action == "start":
                user = User.objects.get(id=self.user_id)
                if user.balance > 0:
                    proxmox.nodes("pve").lxc(self.vm_id).status.start.post()
                else:
                    return False
            elif action == "stop":
                proxmox.nodes("pve").lxc(self.vm_id).status.stop.post()
            return True
        except Exception as e:
            # 处理异常
            print(f"An error occurred while managing vm: {e}")
            return False
    

          
