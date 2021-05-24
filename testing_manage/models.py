from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('电子邮箱是必填的！')
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password)
        user.username = 'admin'
        user.name = 'admin'
        user.is_superuser = True
        user.staff = True
        user.save(using=self._db)
        return user


class CustomUsers(AbstractBaseUser):

    email = models.CharField('电子邮箱', max_length=64, null=False, unique=True)
    username = models.CharField('登录账号', max_length=16, null=False, default='')
    password = models.CharField('账号密码', max_length=128, null=False, unique=True)
    name = models.CharField('你的名字', max_length=16, null=False, default='')
    is_active = models.BooleanField('是否激活', null=False, default=True)
    is_superuser = models.BooleanField('是否是超级管理员',null=False, default=False)
    is_staff = models.BooleanField('是否是管理员', null=False, default=True)

    class Meta:
        db_table = 'users'
        verbose_name = u'用户管理'
        verbose_name_plural = verbose_name
        permissions = ()

    def __str__(self):
        return self.name or self.username or self.email

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
