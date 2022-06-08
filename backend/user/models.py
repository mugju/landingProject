from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# 장고 기본 user를 상속받아 사용
import datetime

# Create your models here.
class UserManager(BaseUserManager):   # 슈퍼유저를 만들어줄 무언가..?
    use_in_migrations = True

    def create_user(self, user_email,  password, user_storename):

        if not user_email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            user_email=self.normalize_email(user_email), # 이메일 정규화
            user_storename = user_storename
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email,  password, user_storename):

        user = self.create_user(
            user_email=self.normalize_email(user_email),
            password=password,
            user_storename = user_storename,
        )
        # user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    user_uid = models.AutoField(primary_key=True)
    user_email = models.EmailField(
        max_length=255,
        unique=True,
    )
    # user_pw = models.CharField(max_length=100)
    user_joindate = models.DateField(auto_now=True)
    user_storename = models.CharField(max_length=20)
    user_session = models.CharField(max_length=30)


    # 추가 컬럼입니다. 이 부분은 회의가 필요합니다..
    login_count = models.PositiveSmallIntegerField(default=0)
    login_blocked_time = models.DateTimeField(null=False, default=datetime.date(1997,10, 1))
    # is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email'
    # PASSWORD_FIELD = 'user_pw'

    REQUIRED_FIELDS = ["user_storename"] # 어드민 생성시 입력받을 값?

    def __str__(self):
        return self.user_email

    @property
    def is_staff(self):
        return self.is_superuser



#  로그기능 추가.
from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


class Logtbl(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Logtbl.objects.create(action='user_logged_in', ip=ip, username=user.user_email)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Logtbl.objects.create(action='user_logged_out', ip=ip, username=user.user_email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Logtbl.objects.create(action='user_login_failed',ip=ip, username=credentials.get('username', None))