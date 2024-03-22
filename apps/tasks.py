from django.conf import settings
from configs.celery import app as celery_app
from .models import User, Uservm
from decimal import Decimal
from .utils import get_time,get_date

@celery_app.task
def daily_free():
    users = User.objects.all()
    for user in users:
        if user.balance < 1:
            user.balance = Decimal(1)
            user.save()

@celery_app.task
def billing_schedule():
    users = User.objects.all()
    for user in users:
        vms = Uservm.objects.filter(user_id=user.id)
        for vm in vms:
            print(vm)
            print(f"{vm.id}status={vm.get_vm_status()}")
            print(f"{vm.id}expire={vm.check_expire()}")
            if vm.get_vm_status() and vm.check_expire():
                user.balance -= Decimal(0.01)
                user.save()
                vm.cost += Decimal(0.01)
                vm.save()
                if user.balance <= 0:
                    vm.manage_vm("stop")
