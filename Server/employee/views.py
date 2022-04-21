from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse

import json
from collections import OrderedDict
from .models import Employee, Salary
from bank.models import Bank  # 은행 uid와  이름 형태 JSON 출력을 위함.
from user.models import User

# DIC 생성 함수들 : models 객체 -> 딕셔너리 형태


# 근로자 JSON 출력

def emp_dic(Data):
    output = dict()

    output["uid"] = Data.emp_uid
    output["emp_name"] = Data.emp_name
    output["emp_joindate"] = str(Data.emp_joindate)
    output["emp_phone"] = Data.emp_phone
    output["emp_address"] = Data.emp_address
    output["emp_added_on"] = str(Data.emp_added_on)
    output["emp_account_no"] = Data.emp_account_no
    output["bank_name"] = Data.bank_uid.bank_name

    sal_data = list(Data.salary_set.values())

    for i in sal_data:      # 조인한 테이블 전처리
        i["sal_date"] = str( i["sal_date"])
        i["sal_joindate"] = str( i["sal_joindate"])
        del i["emp_uid_id"]

    output["emp_salary"] = sal_data

    return output


# 은행 JSON 형태 출력

def bank_dic(Bank, seq):
    output = dict()
    seq = str(seq)  # key 값
    output[seq] = Bank.bank_name

    return output


# employee 생성 함수

def emp_create(request):
    if request.method == 'POST':

        emp_data = json.loads(request.body)  # JSON data parsing

        user = get_object_or_404(User, user_uid = request.session["auth"])
        bank = get_object_or_404(Bank, bank_uid = emp_data["bank_uid"])

        employee = Employee(
            user_uid=user,
            bank_uid=bank,
            emp_name=emp_data["emp_name"],
            emp_joindate=emp_data["emp_joindate"],
            emp_phone=emp_data["emp_phone"],
            emp_address=emp_data["emp_address"],
            emp_account_no=emp_data["emp_account_no"],
            emp_added_on=timezone.now()
        )
        employee.save()
        output = {"message": "Ok"}
    else:
        output = {"message": "Bad request"}

    return output


def edit_employee(request,emp_uid):
    emp_data = json.loads(request.body)  # JSON data parsing

    print("emp_data: {}".format(emp_data))

    employee = get_object_or_404(Employee, emp_uid = emp_uid)
    if employee.emp_uid == request.session['auth']:
        employee.emp_name = emp_data["emp_name"]
        employee.emp_joindate = emp_data["emp_joindate"]
        employee.emp_phone = emp_data["emp_phone"]
        employee.emp_address = emp_data["emp_address"]
        employee.emp_account_no = emp_data["emp_account_no"]
        employee.save()

        Salary.objects.filter(emp_uid = emp_uid).delete()   # 먼저 기존에 있던 데이터를 싹 날려야함.

        bulk_salary = []        # 입력된 연봉정보 한번에 입력
        for ele in emp_data["emp_salary"]:
            new_salary=Salary()
            new_salary.sal_date = ele["sal_date"]
            new_salary.sal_amount = ele["sal_amount"]
            new_salary.sal_joindate = ele["sal_joindate"]
            new_salary.emp_uid = employee
            bulk_salary.append(new_salary)

        Salary.objects.bulk_create(bulk_salary)
        return {"message": "Ok"}
    else:
        return{"message": "Bad request"}


def show_employee (request, page):
    # 은행이름, 직원 , 직원별 급여 총 3개의 테이블을 조인
    emp_ele = Employee.objects.select_related('bank_uid').filter(user_uid=1).prefetch_related('salary_set')

    emp_temp = []  # employee dict 을 담을 배열

    for i in emp_ele:
        emp_temp.append(emp_dic(i))

    output = OrderedDict()
    output["employeeallcount"] = emp_ele.count()  # 요소 전체 갯수

    try:
        if (page - 1) * 10 > len(emp_ele):
            return HttpResponse(json.dumps({"message": "Bad request"}),
                                content_type=u"application/json; charset=utf-8",
                                status=200)
        else:
            output["employee_list"] = emp_temp[(page - 1) * 10: (page - 1) * 10 + 10]

    except Exception as e:
        print("Exception Occured! {}".format(e))
        output["employee_list"] = emp_temp[(page - 1) * 10:]

    bank_dic_all = Bank.objects.all()  # 모든 은행정보를 받아옴.
    bank_temp = []  # bank 정보를 담아둘 배열
    seq = 1  # 은행 uid
    for i in bank_dic_all:
        bank_temp.append(bank_dic(i, seq))
        seq = seq + 1
    output["bank_list"] = bank_temp

    return output


def emp_index(request):
    if request.method == 'GET':  # GET 방식일 경우 딕셔너리 조작후, json 변환 시도.

        try:
            page = int(request.GET.get('page'))
        except Exception as e:
            print("Exception occurred : {}".format(e))      # 페이지 변수 없을 경우
            page = 1

        result = show_employee(request, page)

    elif request.method == 'POST':  # POST 방식일 경우 근로자 만들 수 있어야 함.
        result = emp_create(request)

    else:   # 잘못된 접근
        result = {"message": "Bad request"}

    return HttpResponse(json.dumps(result),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


def emp_detail(request, emp_uid):

    if request.method == 'PATCH':    # 회원정보 수정할경우
        print("근로자 디테일 수정.")
        result = edit_employee(request,emp_uid)
    else:
        result = {"message": "Bad request"}
    return HttpResponse(json.dumps(result),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

