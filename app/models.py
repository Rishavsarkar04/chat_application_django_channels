from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin ,AbstractUser
from app.managers import MyUserManager
from datetime import datetime
# Create your models here.

class MyUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(verbose_name='user name', max_length=255, unique= True)
    email = models.EmailField(verbose_name='email address',max_length=255,blank=True)
    mobile_number = models.CharField(max_length=10 )
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(("staff status"),
        default=False,
        help_text=(
            "Designates that this user can log into the admin site "

        ))

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] #required while creating a superuser

    def __str__(self):
        return self.email
    
class Chat(models.Model):
    sender = models.CharField(max_length=200,blank=True, null=True)
    receiver = models.CharField(max_length=200,blank=True, null=True)
    message = models.TextField(max_length=500,default=None)
    group_name = models.CharField(max_length=250,default=None)
    date_time = models.CharField(max_length=100,default= datetime.now().strftime("%I:%M %p"))
    is_seen = models.BooleanField(default=False)



