from django.shortcuts import render

from django.http import HttpResponse

import json
from django.views import View
from django.http import JsonResponse
from . import models


# Create your views here.

def emp_dic(Employee) : # 근로자 목록 출력
    output = {}

    output["uid"] = Employee.emp_uid
    output["emp_name"] = Employee.emp_name
    output["emp_join"] = Employee.emp_joindate
    output["emp_phone"] = Employee.emp_phone
    output["emp_address"] = Employee.emp_address
    output["emp_addOn"] = Employee.emp_added_on

    return output


def index(request):
    emp_dic_all = models.Employee.objects.all()
    print('employee 총 갯수 : {}'.format(len(emp_dic_all)))

    temp = []

    for i in range(1,len(emp_dic_all)+1):
        print(i)
        temp.append(emp_dic(models.Employee.objects.get(emp_uid=i)))

    print(temp)


    return HttpResponse(temp)

    ## data_test code
    # data = {
    #     "name": "Vaibhav",
    #     "age": 20,
    #     "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"]
    # }
    # return HttpResponse(json.dumps(data), content_type = "application/json")