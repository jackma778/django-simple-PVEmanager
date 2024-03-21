from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db import connection, models, transaction
from decimal import Decimal

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

class UserVPS(models.Model):
    user_id = models.PositiveIntegerField()
    vps_id = models.PositiveIntegerField()
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


          
