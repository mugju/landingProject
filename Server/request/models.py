from django.db import models
from django.utils import timezone

from user import models as USER
# Create your models here.
class Cus_req(models.Model) :
    req_uid = models.AutoField(primary_key=True)
    user_uid  = models.ForeignKey(USER.User, on_delete=models.SET_NULL, db_column='user_uid', null=True)
    req_name = models.CharField(max_length=15  )
    req_phone = models.CharField(max_length=13)
    req_med_detail = models.TextField()
    req_joindate = models.DateTimeField(auto_now_add=True)
    req_status = models.BooleanField(default=False)