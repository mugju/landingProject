from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse

import json
from collections import OrderedDict
from .models import Employee, Salary
from bank.models import Bank  # 은행 uid와  이름 형태 JSON 출력을 위함.
from user.models import User


# employee 출력 함수


def emp_dic(Employee):  # 근로자 JSON 출력
    output = dict()

    output["uid"] = Employee.emp_uid
    output["emp_name"] = Employee.emp_name
    output["emp_join"] = str(Employee.emp_joindate)
    output["emp_phone"] = Employee.emp_phone
    output["emp_address"] = Employee.emp_address
    output["emp_addOn"] = str(Employee.emp_added_on)

    return output


def bank_dic(Bank, seq):  # 은행 JSON 형태 출력
    output = dict()
    seq = str(seq)  # key 값
    output[seq] = Bank.bank_name

    return output


# employee 생성 함수


def emp_create(request, user_uid):
    user_num = get_object_or_404(User, pk=user_uid)
    print('해당 하는 object num{}'.format(user_num))  # 값 확인해 보려고
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


def add_salary(request, emp_uid):
    print("급여 추가")
    get_object_or_404(Employee, pk=emp_uid)


def edit_salary(request):
    print("급여 수정")


def delete_salary(request, sal_uid):
    print("인자 받아 와서 바로 삭제함. sal_uid 받야야 함. ")


def emp_index(request):
    if request.method == 'GET':  # GET 방식일 경우 딕셔너리 조작후, json 변환 시도.
        # model 을 2N번  접근하는 현재 문제에 대한 개선 필요.

        emp_dic_all = Employee.objects.filter(user_uid=1)  # 유저에 해당하는 직원만 받아와야 하기에 필터설정

        emp_temp = []  # employee dict을 담을 배열

        for i in emp_dic_all:
            emp_temp.append(emp_dic(i))

        bank_dic_all = Bank.objects.all()  # 모든 은행정보를 받아옴.

        bank_temp = []  # bank 정보를 담아둘 배열
        for i in range(1, len(bank_dic_all) + 1):
            bank_temp.append(bank_dic(Bank.objects.get(bank_uid=i), i))

        output = OrderedDict()
        output["employee_list"] = emp_temp
        output["bank_list"] = bank_temp
        print(json.dumps(output, ensure_ascii=False, indent="\t"))
        result = json.dumps(output, ensure_ascii=False, indent="\t")
        return HttpResponse(result,
                            content_type=u"application/json; charset=utf-8",
                            status=200)

    if request.method == 'POST':  # POST 방식일 경우
        print("근로자 만드는 함수 돌리쟈")
        emp_create(request, request.POST.get('user_uid'))


def emp_detail(request, emp_uid):
    if request.method == 'GET':  # employee -> views
        emp = emp_dic(Employee.objects.get(emp_uid=emp_uid))

    emp = json.dumps(emp, ensure_ascii=False, indent="\t")
    return HttpResponse(emp,
                        content_type=u"application/json; charset=utf-8",
                        status=200)  # json 형태 output으로 바꿔줘야함.
