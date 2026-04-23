from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_permissions_set',
        related_query_name='customuser_permission',
    )

    def __str__(self):
        return self.username