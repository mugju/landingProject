from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse

import json
from collections import OrderedDict
from .models import Employee, Salary
from bank.models import Bank  # 은행 uid와  이름 형태 JSON 출력을 위함.
from user.models import User


# DIC 생성 함수들  models 객체 -> 딕셔너리 형태


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


def sal_dic(Salary):  # 급여 json 출력
    output = dict()
    output["sal_uid"] = Salary.sal_uid
    output["sal_date"] = str(Salary.sal_date)
    output["sal_amount"] = Salary.sal_amount
    output["sal_addOn"] = str(Salary.sal_joindate)

    return output


# ================= dict 생성함수 선언 끝 ==========================


# employee 생성 함수

def emp_create(request):
    # 외래 키의 경우 무조건 해당 모델의 인스 턴스를 집어 넣어야 하므로 임의의 값을
    # 생성 해서 넣어 주도록 한다.

    sample_useruid = User.objects.get(user_uid=1)  # 현재 세션이 따로 없기 때문에 넣어준 값
    sample_bankuid = Bank.objects.get(bank_uid=1)

    emp_data = json.loads(request.body)  # JSON data parsing

    employee = Employee(
        user_uid=sample_useruid,
        bank_uid=sample_bankuid,
        emp_name=emp_data["emp_name"],
        emp_joindate=emp_data["emp_joindate"],
        emp_phone=emp_data["emp_phone"],
        emp_address=emp_data["emp_address"],
        emp_account_no=emp_data["emp_account_no"],
        emp_added_on=timezone.now()
    )
    employee.save()
    return "ok"


# 직원 정보 수정 함수 , 급여 수정 포함.

def edit_employee(request, emp_uid):    # emp_uid는 url 상에서 받아옴.
    emp_data = json.loads(request.body)  # JSON data parsing
    print("emp_data: {}".format(emp_data))

    employee = Employee.objects.get(emp_uid=emp_uid)
    employee.emp_name = emp_data["emp_name"]
    employee.emp_joindate = emp_data["emp_joindate"]
    employee.emp_phone = emp_data["emp_phone"]
    employee.emp_address = emp_data["emp_address"]
    employee.emp_account_no = emp_data["emp_account_no"]
    employee.save()

    for sal in emp_data['emp_salary']:
        print(sal)
        try:
            salary = Salary.objects.get(sal_uid=sal["sal_uid"])     # 만약없는 uid 일경우 0으로 하거나 음수값 넣어주세요.
            salary.sal_date = sal["sal_date"]
            salary.sal_amount = sal["sal_amount"]
            salary.sal_joindate = sal["sal_addOn"]
        except :    #새로운 급여목록일 경우
            print("new salary!")
            salary = Salary(
                sal_date=sal["sal_date"],
                sal_amount = sal["sal_amount"],
                sal_joindate = sal["sal_addOn"],
                emp_uid = employee
            )
            
        salary.save()
    return "ok"

def emp_del(request,emp_uid):
    employee =get_object_or_404(Employee,emp_uid=emp_uid)
    employee.delete()
    return "ok"

def emp_index(request):
    if request.method == 'GET':  # GET 방식일 경우 딕셔너리 조작후, json 변환 시도.

        emp_dic_all = Employee.objects.filter(user_uid=1)  # 유저에 해당하는 직원만 받아와야 하기에 필터설정

        emp_temp = []  # employee dict을 담을 배열

        for i in emp_dic_all:
            emp_temp.append(emp_dic(i))

        bank_dic_all = Bank.objects.all()  # 모든 은행정보를 받아옴.
        bank_temp = []  # bank 정보를 담아둘 배열

        seq = 1  # 은행 uid
        for i in bank_dic_all:
            bank_temp.append(bank_dic(i, seq))
            seq = seq + 1

        # dic -> json 형태로 변환
        output = OrderedDict()
        output["employee_list"] = emp_temp
        output["bank_list"] = bank_temp
        print(json.dumps(output, ensure_ascii=False, indent="\t"))
        result = json.dumps(output, ensure_ascii=False, indent="\t")
        return HttpResponse(result,
                            content_type=u"application/json; charset=utf-8",
                            status=200)

    if request.method == 'POST':  # POST 방식일 경우 근로자 만들 수 있어야 함.
        print("근로자 만드는 함수 돌리쟈")
        output = emp_create(request)  # 현재 함수 탈출이 안됨

        return HttpResponse(output,
                            content_type=u"application/json; charset=utf-8",
                            status=200)


def emp_detail(request, emp_uid):   # employee 상세보기 페이지, 수정도 겸함.
    if request.method == 'GET':  # employee -> views  // 직원 상세보기/.
        emp = emp_dic(Employee.objects.get(emp_uid=emp_uid))
        sal_dic_all = Salary.objects.filter(emp_uid=emp_uid)

        sal_list = []       # 연봉정보가 들어갈 리스트.
        for i in sal_dic_all:
            sal_list.append(sal_dic(i))

        emp["emp_salary"] = sal_list    # 기존 dict 형식에 연봉 키값 추가.

        emp = json.dumps(emp, ensure_ascii=False, indent="\t")
        return HttpResponse(emp,
                            content_type=u"application/json; charset=utf-8",
                            status=200)  # json 형태 output으로 바꿔줘야함.

    if request.method == 'PATCH':  # 회원정보 수정할경우
        print("근로자 디테일 수정.")
        result = edit_employee(request, emp_uid)
        output = {
            "message" : result
        }
        return HttpResponse(json.dumps(output),
                            content_type=u"application/json; charset=utf-8",
                            status=200)

    if request.method=='DELETE':
        result = emp_del(request, emp_uid)
        output = {
            "message": result
        }
        return HttpResponse(json.dumps(output),
                            content_type=u"application/json; charset=utf-8",
                            status=200)