from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse

import json
from collections import OrderedDict
from .models import Employee, Salary
from bank.models import Bank  # 은행 uid와  이름 형태 JSON 출력을 위함.
from user.models import User

from user.views import check_session

# DIC 생성 함수들 : models 객체 -> 딕셔너리 형태

# ========employee JSON 생성함수 =================

def emp_dic(Data):
    """
            employee 인원 정보를 dict 형태로 정리하는 함수

                Args:
                    Data(json) : 클라이언트로 부터의 요청

                Returns:
                    output (json)   :  employee dict 정보보

           """
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
        i["sal_date"] = str( i["sal_date"])     #문자열 자동 변환이 안되서 명시적으로 실행해줌
        i["sal_joindate"] = str( i["sal_joindate"])
        del i["emp_uid_id"]     #자동 정렬하면서 생기는 컬럼

    output["emp_salary"] = sal_data

    return output

# ==========은행 JSON 형태 출력=================

def bank_dic(Bank, seq):
    """
                bank 정보를 dict 형태로 정리하는 함수

                    Args:
                        Bank(model) : bank 모델 객체

                        seq(int) : 은행별 고유 id

                    Returns:
                        output (json)   :  bank dict 정보

               """
    output = dict()
    seq = str(seq)  # key 값
    output[seq] = Bank.bank_name

    return output


# ============employee 생성 함수===============

def emp_create(request):
    """
            유저 수정함수

                Args:
                    request : 클라이언트로 부터의 요청

                Returns:
                    output (json)   :  유저정보 수정 여부를 반환함.

                Raises:
                    400 {"message" : "Bad request" } : 입력값이 잘못된 경우

                    403 {"message" : "session ID not found" } : 저장된 세션정보가 없는 경우

                    405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
            """
    if request.method == 'POST':
        useruid = check_session(request)
        if useruid == 0:
            return {'message': 'session ID not found'}, 403

        emp_data = json.loads(request.body)  # JSON data parsing
        user = get_object_or_404(User, user_uid = useruid)
        bank = get_object_or_404(Bank, bank_uid = emp_data["bank_uid"])

        count = Employee.objects.filter(emp_phone = emp_data["emp_phone"]).count()
        count = count + Employee.objects.filter(emp_account_no = emp_data["emp_account_no"]).count()
        if count > 0:
            return {'message': 'bad input data'}, 400
        employee = Employee(
            user_uid=user,
            bank_uid=bank,
            emp_name=emp_data["emp_name"],
            emp_joindate=emp_data["emp_joindate"],
            emp_phone=emp_data["emp_phone"],
            emp_address=emp_data["emp_address"],
            emp_account_no=emp_data["emp_account_no"],
            # emp_added_on=timezone.now()
            emp_added_on=emp_data["emp_added_on"]
        )
        try:    # save 쿼리를 쳤으나, 잘못된 데이터일 경우
            employee.save()
            output = {"message": "Ok"}
            CODE = 200
        except Exception as e:
            print(e)
            output = {"message": "bad input data"}
            CODE = 400

    else:
        output = {"message": "method not allowed"}
        CODE = 405

    return output, CODE


# =============근로자 정보 수정================

def edit_employee(request,emp_uid):
    """
                유저 수정함수

                    Args:
                        request : 클라이언트로 부터의 요청

                    Returns:
                        output (json)   :  유저정보 수정 여부를 반환함.

                    Raises:
                        400 {"message" : "Bad request" } : 입력값이 잘못된 경우

                        403 {"message" : "session ID not found" } : 저장된 세션정보가 없는 경우

                        405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
                """
    emp_data = json.loads(request.body)  # JSON data parsing
    employee = get_object_or_404(Employee, emp_uid = emp_uid)

    useruid = check_session(request)
    if useruid == 0:
        return {'message': 'session ID not found'}, 403
    if employee.user_uid_id == useruid: # 수정하고자 하는 정보가 유저에게 속한 정보일경우


        try:
            employee.emp_name = emp_data["emp_name"]
            employee.emp_joindate = emp_data["emp_joindate"]
            employee.emp_phone = emp_data["emp_phone"]
            employee.emp_address = emp_data["emp_address"]
            employee.emp_account_no = emp_data["emp_account_no"]
            employee.bank_uid = Bank.objects.get(bank_uid = emp_data["bank_uid"])
            employee.save()

            #날리기 전에 백업하고..
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
            return {"message": "Ok"},200

        except Exception as e:
            print("error occured!! : ",e)
            return {"message": "bad input data"}, 400
    else:
        return{"message": "unauthorized"},401


# =============근로자 정보 삭제=================
def delete_employee (request, emp_uid) :
    """
                    유저 수정함수

                        Args:
                            request : 클라이언트로 부터의 요청

                            emp_uid : employee uid

                        Returns:
                            output (json)   :  근로자 정보 삭제 여부를 반환함.

                        Raises:
                            400 {"message" : "Bad request" } : 입력값이 잘못된 경우

                            403 {"message" : "session ID not found" } : 저장된 세션정보가 없는 경우

                            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
                    """
    useruid = check_session(request)
    if useruid == 0:
        return {'message': 'session ID not found'}, 403
    employee = get_object_or_404(Employee, emp_uid = emp_uid)
    if employee.user_uid_id ==  useruid :
        employee.delete()
    else :
        return {"message": "unauthorized"}, 401

    return{"message": "ok"}, 200


def show_employee (request, page):
    """
    유저 정보 확인 함수

        Args:
            request : 클라이언트로 부터의 요청
            page : 보고자 하는 페이지

        Returns:
            output (json)   :  근로자 정보 삭제 여부를 반환함.

        Raises:
            400 {"message" : "Bad request" } : 입력값이 잘못된 경우

            403 {"message" : "session ID not found" } : 저장된 세션정보가 없는 경우

            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
    """
    useruid = check_session(request)
    if useruid == 0:
        return {'message': 'session ID not found'}, 403
    # 은행이름, 직원 , 직원별 급여 총 3개의 테이블을 조인
    emp_ele = Employee.objects.select_related('bank_uid').filter(user_uid=useruid).prefetch_related('salary_set')

    emp_temp = []  # employee dict 을 담을 배열
    for i in emp_ele:
        emp_temp.append(emp_dic(i))

    output = OrderedDict()
    output["employeeallcount"] = emp_ele.count()  # employee 요소 전체 갯수

    # 페이징 관련 코드
    try:
        if (page - 1) * 10 > len(emp_ele):
            return JsonResponse({"message": "Bad request"}, status=404)
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
    CODE = 200
    return output,CODE


# 뒤에 uid가 안붙는 view 함수  ex) show 함수, create 함수
def emp_index(request):
    """
    유저 확인 및 생성 분기 함수
    
        Args:
            request: 클라이언트 요청
            
        Returns:
            output (json)   :
                GET : employee list 출력함수 성공여부

                POST : employee 생성 함수 성공 여부

        Raises:

            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
    """
    if request.method == 'GET':  # GET 방식일 경우 딕셔너리 조작후, json 변환 시도.
        try:
            page = int(request.GET.get('page'))
        except Exception as e:
            print("Exception occurred : {}".format(e))      # 페이지 변수 없을 경우
            page = 1
        result, CODE = show_employee(request, page)

    elif request.method == 'POST':  # POST 방식일 경우 근로자 만들 수 있어야 함.
        result,CODE = emp_create(request)

    else:   # 잘못된 접근
        result = {"message": "method not allowed"}
        CODE = 405

    return JsonResponse(result, status=CODE)


# 뒤에 uid 가 붙는 함수  ex ) 정보 수정 , 정보 삭제 함수
def emp_detail(request, emp_uid):
    """
        근로자 정보 수정 및 삭제 분기 함수

            Args:
                request : 클라이언트 요청

            Returns:
                output (json)   :
                    PATCH : employee 수정 함수 실행 성공여부를 나타냄.
                    DELETE : employee 삭제함수 실행 성공여부를 나타냄.

            Raises:
                405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
        """
    if request.method == 'PATCH':    # 회원정보 수정할경우
        result,CODE = edit_employee(request,emp_uid)

    elif request.method == 'DELETE':
        result,CODE = delete_employee(request, emp_uid)
    else:
        result = {"message": "method not allowed"}
        CODE = 405
    return JsonResponse(result, status=CODE)

