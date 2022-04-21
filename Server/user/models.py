
# 장고 기본 user를 상속받아 사용
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):     #슈퍼유저를 만들어줄 무언가..?
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

    def create_superuser(self, user_email,  password, storename):

        user = self.create_user(
            user_email=self.normalize_email(user_email),
            password=password,
            storename = "슈퍼유저"
        )
        user.is_admin = True
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
    user_joindate = models.DateTimeField(auto_now=True)
    user_storename = models.CharField(max_length=20)
    user_session = models.CharField(max_length=30)


    # 추가 컬럼입니다. 이 부분은 회의가 필요합니다..
    login_count = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email'
    # PASSWORD_FIELD = 'user_pw'

    REQUIRED_FIELDS = [] # 어드민 생성시 입력받을 값?

    def __str__(self):
        return self.user_email

    @property
    def is_staff(self):
        return self.is_admin




# class User(models.Model):
#     user_uid = models.AutoField(primary_key=True)
#     user_email = models.EmailField()
#     user_pw = models.CharField(max_length=100)
#     user_joindate = models.DateTimeField(auto_now=True)
#     user_storename = models.CharField(max_length=20)
#     user_session = models.CharField(max_length=30)
