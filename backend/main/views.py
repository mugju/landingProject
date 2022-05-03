from django.shortcuts import render
from django.http import HttpResponse
from user.models import User
from bill.models import Bill
from employee.models import Employee
from medicine.models import Medicine
from company.models import Company

from datetime import date, timedelta, datetime

from user.views import main_data,date_range
import json

# Create your views here.

def index(request) :
    if request.session['auth']:
        user_info = User.objects.get(user_uid = request.session['auth'])
        bill_data = Bill.objects.filter(user_uid=request.session['auth'],
                                        bill_date__range=[date.today() - timedelta(days=4), date.today()])

        med_data = Medicine.objects.filter(user_uid=request.session['auth'])
        emp_data = Employee.objects.filter(user_uid=request.session['auth'])
        com_data = Company.objects.filter(user_uid=request.session['auth'])

        output = main_data(user_info, bill_data, med_data, emp_data, com_data)

        return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)
    else:
        output = {"message": "Bad request"}
        return HttpResponse(json.dumps(output),
                            content_type=u"application/json; charset=utf-8",
                            status=400)
