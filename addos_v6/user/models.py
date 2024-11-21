from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, blank=True)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=True, null=True)

    USERNAME_FIELD = 'email'  # 이메일을 username으로 사용
    REQUIRED_FIELDS = ['nickname', 'ip_address']

    objects = CustomUserManager()  # 커스텀 매니저 추가

    def __str__(self):
        return self.email
