from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse

import json
from django.views import View
from django.http import JsonResponse
from .models import Employee, Salary
from user.models import User

# Create your views here.
# employee 출력 함수


def emp_dic(Employee) : # 근로자 목록 출력
    output = dict()

    output["uid"] = Employee.emp_uid
    output["emp_name"] = Employee.emp_name
    output["emp_join"] = Employee.emp_joindate
    output["emp_phone"] = Employee.emp_phone
    output["emp_address"] = Employee.emp_address
    output["emp_addOn"] = Employee.emp_added_on

    return output


# employee 생성 함수


def emp_create(request,user_uid) :
    user_num = get_object_or_404(User, pk=user_uid)
    print('해당 하는 object num{}'.format(user_num))     # 값 확인해 보려고
    employee = Employee(
        user_uid=user_uid,
        bank_uid=request.POST.get('bank_uid'),
        emp_name=request.POST.get('emp_name'),
        emp_joindate=request.POST.get('emp_join'),
        emp_phone=request.POST.get('emp_phone'),
        emp_address=request.POST.get('emp_address'),
        emp_account_no=request.POST.get('emp_account'),
        emp_added_on=timezone.now()
    )
    employee.save()
    return redirect('employee/')

def edit_employee(request, emp_uid):
    print("인자 받아 와서 근로자 uid 기반 으로 수정 들어감")
    employee = get_object_or_404(Employee, pk=emp_uid)
    employee.emp_name = request.POST.get("emp_name")
    employee.emp_joindate = request.POST.get('emp_join')
    employee.emp_phone = request.POST.get('emp_phone')
    employee.emp_address = request.POST.get('emp_address')
    employee.emp_account_no = request.POST.get('emp_account')

    employee.save()




def add_salary(request,emp_uid):
    print("급여 추가")
    get_object_or_404(Employee, pk=emp_uid)


def edit_salary(request):
    print("급여 수정")


def delete_salary(request, sal_uid):
    print("인자 받아 와서 바로 삭제함. sal_uid 받야야 함. ")






def emp_index(request):
    if request.method == 'GET':     # GET 방식일 경우

        emp_dic_all = Employee.objects.all()
        print('employee 총 갯수 : {}'.format(len(emp_dic_all)))

        temp = []

        for i in range(1,len(emp_dic_all)+1):
            print(i)
            temp.append(emp_dic(Employee.objects.get(emp_uid=i)))

        print(temp)
        return HttpResponse(temp)

    if request.method == 'POST':  # POST 방식일 경우
        print("근로자 만드는 함수 돌리쟈")
        emp_create(request, request.POST.get('user_uid'))


def emp_detail(request, emp_uid) :
    if request.method == 'GET' :         # employee -> views
        emp = emp_dic(Employee.objects.get(emp_uid = emp_uid ))
        print('employee 정보 : {}'.format(emp))

    return HttpResponse(emp)        # json 형태 output으로 바꿔줘야함.


