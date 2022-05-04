from django.db import models
from user import models as USER
from bank import models as BANK

# Create your models here.


class Employee(models.Model):
    emp_uid = models.AutoField(primary_key=True)
    user_uid = models.ForeignKey(USER.User, on_delete=models.CASCADE, db_column='user_uid')
    bank_uid = models.ForeignKey(BANK.Bank, on_delete= models.SET_NULL, db_column='bank_uid',null=True)
    emp_name = models.CharField(max_length=15)
    emp_joindate = models.DateField()
    emp_phone = models.CharField(max_length=15)
    emp_address = models.CharField(max_length=50)
    emp_account_no = models.CharField(max_length=20)
    emp_added_on = models.DateField(auto_now_add="True")


class Salary(models.Model):
    sal_uid = models.AutoField(primary_key = True)
    emp_uid = models.ForeignKey(Employee, related_name='salary_set',on_delete=models.CASCADE, db_column='emp_uid')      # related name 옵션이 추가되었음.
    sal_date = models.DateField()
    sal_amount = models.PositiveIntegerField()
    sal_joindate = models.DateField(auto_now_add=True)
