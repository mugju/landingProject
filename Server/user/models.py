from django.db import models

# Create your models here.

class User(models.Model):
    user_uid = models.AutoField(primary_key=True)
    user_email = models.EmailField()
    user_pw = models.CharField(max_length=100)
    user_joindate = models.DateTimeField(auto_now=True)
    user_storename = models.CharField(max_length=20)
    user_session = models.CharField(max_length=30)
