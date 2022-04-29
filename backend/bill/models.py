from django.db import models
from user import models as USER

# Create your models here.
class Bill(models.Model):
    bill_uid = models.AutoField(primary_key=True)
    user_uid = models.ForeignKey(USER.User, on_delete=models.SET_NULL,db_column='user_uid',null=True)
    bill_total_sell = models.PositiveIntegerField(null=True)
    bill_profit = models.PositiveIntegerField(null=True)
    bill_date = models.DateField(null=True)

