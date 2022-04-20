from django.db import models

from user import models as USER # user_uid 사용하기 위함

# Create your models here.
class Medicine(models.Model) :
    med_uid = models.AutoField(primary_key=True)
    user_uid = models.ForeignKey(USER.User,on_delete=models.SET_NULL,db_column='user_uid',null=True)
    med_name = models.CharField(max_length=20)
    med_type = models.CharField(max_length=8)
    med_buyprice = models.PositiveIntegerField()
    med_sellprice = models.PositiveIntegerField()
    med_cgst = models.PositiveSmallIntegerField()   #세율의 경우 작을 것이라 예상
    med_sgst = models.PositiveSmallIntegerField()   # ref : https://docs.djangoproject.com/en/4.0/ref/models/fields/
    med_expire = models.DateField()
    med_mfg = models.DateField()
    med_desc = models.TextField()
    med_instock = models.PositiveIntegerField()
    med_qty = models.PositiveSmallIntegerField()
    med_company = models.CharField(max_length=30)

class Med_salt(models.Model) :
    salt_uid = models.AutoField(primary_key=True)
    med_uid = models.ForeignKey(Medicine, on_delete=models.CASCADE, db_column='med_uid')
    salt_name = models.CharField(max_length=20)
    salt_qty = models.DecimalField(max_digits=5, decimal_places=3) #다섯자리까지, 소숫점 셋째자리까지
    salt_qty_type = models.CharField(max_length=20)
    salt_desc = models.TextField()