from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# CUSTOM USER MANAGER MODEL
class UserManager(BaseUserManager):
    def create_user(self, username, token, password=None):
        if not username:
            raise ValueError("USERNAME MISSING")
        if not token:
            raise ValueError("TOKEN MISSING")
        user = self.model(username=username, token=token)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, token, password):
        user = self.create_user(username=username, token=token, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# CUSTOM USER MODEL
class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=20, unique=True)
    token = models.CharField(verbose_name="token", max_length=40, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# REPOSITORY MODEL
class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(verbose_name='repo owner', max_length=39)
    name = models.CharField(verbose_name='repo name', max_length=40)
    url = models.CharField(verbose_name='repo url', max_length=180)

    def __str__(self):
        return self.owner + "/" + self.name
