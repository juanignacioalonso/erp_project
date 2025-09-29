from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150,unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Role(models.Model):
    PERMISSION_CHOISES = [
        (0,'No access'),
        (1,'View only'),
        (0,'Create an modify'),
    ]

    role_name = models.CharField(max_length=50,primary_key=True)
    customers = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    suppliers = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    materials = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    purchases = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    sales = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    inventory = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    accounting = models.IntegerField(choices=PERMISSION_CHOISES,default=0)
    reporting = models.IntegerField(choices=PERMISSION_CHOISES,default=0)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name
    
class UserRole(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        unique_together = ('user_id','role')

    def __str__(self):
        return f"{self.user_id.username} - {self.role.role_name}"