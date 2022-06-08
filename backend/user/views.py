from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate
import json
from .models import User
from bill.models import Bill
from employee.models import Employee
from medicine.models import Medicine
from company.models import Company
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse, JsonResponse

# 날짜 관련
from datetime import date, timedelta, datetime



def date_range(start, end):
    """  메인 화면 sell/profit chart 에서 날짜 범위를 나타내기 위한 함수

        Args:
            start (datetime): 차트 시작 날짜
            end (datetime): 차트 마지막 날짜

        Returns:
            list()  :  날짜 범위를 list 형태로 뿌려줌

        Raises:
            해당 사항 없음.
        """
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates


from django.db.models import Sum

def check_session(request)  :
    """  세션아이디를 확인하는 함수. 없을시에는 0 반환 , 있을시에는 user uid 반환

        Args:
            request: 클라이언트 로 부터의 요청

        Returns:
            user_uid  :  세션에 저장된 user_uid 반환. (해당 uid 가 존재 하지 않을 경우에는 0 반환)

        """
    try:
        user_uid = request.session['auth']
        print("user session : {}".format(user_uid))
        return user_uid
    except :
        return 0



# ===============메인화면 관련 ======================

def main_data(user_data, bill_data,med_data, emp_data,com_data):  
    """  로그인 및 회원가입시 메인화면에 나타내줄 데이터 셋을 만드는 함수

        Args:
            user_data: 현재 로그인한 user 에 대한 모델 객체
            bill_data:  bill 모델 객체
            med_data:   medicine 모델 객체
            emp_data:   employee 모델 객체
            com_data:   company 모델 객체

        Returns:
             output (json)   :  API 문서에 따른 user 정보와 request 정보, medicine 정보 포함/ 차트 생성에 필요한  json 데이터 포함.
    """
    output = dict()
    output["user_uid"] = user_data[0].user_uid
    output["user_storename"] = user_data[0].user_storename
    output["user_email"] = user_data[0].user_email
    output["user_totalreqs"] = user_data[0].req_set.count()
    output["total_medicine"]  = med_data.count()
    output["user_completedreq"] = user_data[0].req_set.filter(req_status=True).count()
    output["user_pendingreq"] = user_data[0].req_set.filter(req_status=False).count()
    output["total_employee"] = emp_data.count()
    output["total_company"] = com_data.count()

    profit_arr = list() # json 생성용
    sell_arr = list()

    for day in date_range(str(date.today() - timedelta(days=4)), str(date.today())):
        dic_profit = dict()
        dic_profit["date"] = day
        dic_profit["won"] = bill_data.filter(bill_date=day).aggregate(Sum('bill_profit'))["bill_profit__sum"]
        profit_arr.append(dic_profit)
        
        dic_sell = dict()
        dic_sell["date"] = day
        dic_sell["won"] = bill_data.filter(bill_date=day).aggregate(Sum('bill_total_sell'))["bill_total_sell__sum"]
        sell_arr.append(dic_sell)
    output['bill_profit'] = profit_arr
    output['bill_total_sell'] = sell_arr

    return output


# ==============로그인 함수=================
@method_decorator(csrf_exempt, name='dispatch')
def signin(request):
    """
    로그인 함수 / 로그인이 진행되면 세션에 데이터를 저장한다.
        Args:
            request : 클라이언트로 부터의 요청

        Returns:
            output (json)   :  API 문서에 따른 user 정보와 request 정보, medicine 정보 포함/ 차트 생성에 필요한  json 데이터 포함.

        Raises:
            401 {"message" : "user is lock","useTime": xx:xx:xx } : 계정이 5회 틀림으로 인해 잠김 상태일 경우

            404 {"message" : "user not found" } : 해당하는 계정 정보를 찾을 수 없는 경우

            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
    """
    if request.ethod == "POST":  # 정상적인 접근
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email = user_data["user_email"]
        user_password = user_data["user_pw"]

        user = authenticate(request, password=user_password, username=user_email)  # 유저 인증과정
        if user is None:  # 회원정보 없는 경우.
            try: # 이메일은 맞고, 비밀번호는 틀린 경우
                ui = User.objects.get(user_email = user_email)
                if ui.login_blocked_time > datetime.now():      # 계정이 블록된 상태인지 아닌지 확인
                    return HttpResponse(json.dumps({"message": "user is lock","useTime": ui.login_blocked_time.strftime("%Y-%m-%d %H:%M:%S")}),
                                        content_type=u"application/json",
                                        status=401)

                ui.login_count = ui.login_count + 1
                ui.save()

                # 로그인 블록시간
                if (ui.login_count % 5) == 0: # 5의 배수일경우
                    ui.login_blocked_time = datetime.now() + timedelta(minutes=30)
                    ui.save()

            except: pass # 없는 유저 이메일일 경우 => 그냥 404 띄워버리면 된다.

            return HttpResponse(json.dumps({"message": "user not found"}),
                                content_type=u"application/json; charset=utf-8",
                                status=404)

        else:  # 회원정보가 정상적인 경우.
            if user.login_blocked_time > datetime.now():
                return HttpResponse(json.dumps({"message" : "user is lock","useTime": user.login_blocked_time.strftime("%Y-%m-%d %H:%M:%S")}),
                                    content_type=u"application/json; charset=utf-8",
                                    status=401)

            auth.login(request, user)
            user.login_count = 0
            user.save()
            request.session['auth'] = user.user_uid  # 세션을 통해 uid 넘겨줌
            print("user auth : ", request.session['auth'])

        user_info = User.objects.filter(user_uid=user.user_uid).prefetch_related('req_set')

        bill_data = Bill.objects.filter(user_uid=user.user_uid,
                                        bill_date__range=[date.today() - timedelta(days=4), date.today()])
        med_data = Medicine.objects.filter(user_uid = user.user_uid)
        emp_data = Employee.objects.filter(user_uid = user.user_uid)
        com_data = Company.objects.filter(user_uid = user.user_uid)
        output = main_data(user_info, bill_data,med_data, emp_data,com_data)
    else:
        output = {"message": "method not allowed"}
        return HttpResponse(json.dumps(output),
                            content_type=u"application/json; charset=utf-8",
                            status=405)

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


# ===============회원가입 함수===============
@method_decorator(csrf_exempt, name='dispatch')
def signup(request):
    """
        회원가입 함수/ 적절한 회원정보가 작성된 경우 DB에 회원을 생성한다.
            Args:
                request : 클라이언트로 부터의 요청

            Returns:
                output (json)   :  API 문서에 따른 user 정보와 request 정보, medicine 정보 포함/ 차트 생성에 필요한  json 데이터 포함.

            Raises:
                400 {"message" : "email duplicates" } : 회원가입시 작성한 email 이 이미 존재하는 email 일 경우

                401 {"message": "Password authorization failed"} : 비밀번호 확인 과정에서 같은 비밀번호가 입력되지 않은 경우

                405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
        """
    if request.method == 'POST':
        user_data = json.loads(request.body)  # JSON data parsing / 여기 에선 회원 가입 정보.

        # 이메일 중복된 경우
        try:
            User.objects.get(user_email = user_data["user_email"])
            return HttpResponse(json.dumps({"email_duplicatied": True}),
                                content_type=u"application/json; charset=utf-8",
                                status=400)
        except:
            pass # 없는경우


        if user_data["user_pw"] == user_data["user_pw_confirm"]:  # 비밀번호 확인
            user = User.objects.create_user(
                user_email=user_data["user_email"],
                password=user_data["user_pw"],
                user_storename=user_data["user_storename"]
            )
            auth.login(request, user)
            request.session['auth'] = user.user_uid  # 세션을 통해 uid 넘겨줌

            user_info = User.objects.filter(user_uid=user.user_uid).prefetch_related('req_set')
            bill_data = Bill.objects.filter(user_uid=user.user_uid,
                                            bill_date__range=[date.today() - timedelta(days=4), date.today()])
            med_data = Medicine.objects.filter(user_uid=user.user_uid)
            emp_data = Employee.objects.filter(user_uid=user.user_uid)
            com_data = Company.objects.filter(user_uid=user.user_uid)
            output = main_data(user_info, bill_data,med_data, emp_data, com_data)
            CODE = 200

        else:  # 비밀 번호가 같지 않은 경우.
            output = {"message": "Password authorization failed"}; CODE = 401

    else:  # post 이외 방식 으로 접근 한 경우.
        output = {"message": "method not allowed"}; CODE = 405

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=CODE)


# 패스 워드 찾기 함수 ==> 회원 정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
    """
    패스워드 찾는 함수 / 회원 email 과 storename을 기반으로 비밀번호 재설정 대상 session을 반환함.
                Args:
                    request : 클라이언트로 부터의 요청

                Returns:
                    output (json)   :  비밀번호 변경 가능 여부를 반환함.

                Raises:
                    400 {"message" : "Bad request" } : 입력값이 잘못된 경우

                    401 {"message": "Incorrect user storename"} : 회원정보 확인 과정에서 잘못된 정보가 입력된 경우

                    405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
    """
    if request.method == 'POST':
        user_data = json.loads(request.body)

        # 입력정보 기반 db에서 회원정보 탐색.
        user = get_object_or_404(User, user_email=user_data["user_email"])

        if user.user_storename == user_data["user_storename"]:
            request.session['auth'] = user.user_uid
            output = {"message": "ok"}; CODE = 200

        else:
            output = {"message": "Incorrect user storename"}; CODE = 401

    else:
        output = {"message": "Bad request"}; CODE = 400

    return JsonResponse(output,status=CODE)

# =========패스 워드 재설정 ==> 유저 정보 찾은 이후에 가능함.===========

def pw_set(request):
    """

    패스워드 재설정 함수 / pw_find 함수가 선행되어야 함
        Args:
            request : 클라이언트로 부터의 요청

        Returns:
            output (json)   :  비밀번호 변경 여부를 반환함.

        Raises:
            400 {"message" : "Bad request" } : 입력값이 잘못된 경우

            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
    """
    if request.method == 'POST':
        try:
            user_uid = check_session(request)
            user = get_object_or_404(User, user_uid=user_uid)
            new_pw = json.loads(request.body)["user_new_pw"]

            user.set_password(new_pw)
            user.save()
            output = {"message": "Ok"}; CODE = 200

        except Exception as e:
            print(e)
            output = {"message": "Bad request"}; CODE = 400
    else:
        output = {"message": "method not allowed"}; CODE = 405

    return JsonResponse(output,status = CODE)


# =================유저 삭제 함수================

def delete_user(request, user_uid):  # 슈퍼 유저 혹은 본인 이어야 회원 탈퇴 가능
    """
    유저 삭제함수
        Args:
            request : 클라이언트로 부터의 요청

        Returns:
            output (json)   :  유저 삭제 여부를 반환함.

        Raises:
            400 {"message" : "Bad request" } : 입력값이 잘못된 경우

            401 {"message" : "session ID not found"} :  권한이 없는 경우
    """
    session_uid = check_session(request)
    if session_uid == 0 :
        return {'message': 'session ID not found'}, 401

    user = get_object_or_404(User, user_uid=session_uid)

    if user.is_superuser == 1 or user.user_uid == session_uid:  # 어드민 이거나, 본인일 경우에 삭제 가능.
        User.objects.get(user_uid=user_uid).delete() # 찾아서 삭제함.
        return {"message": "Ok"}, 200
    else:
        return {"message": "unauthorized"}, 401


# ==============유저 정보 수정=====================

def edit_user(request, user_uid):
    """
        유저 수정함수
            Allowed Method:
                PATCH , DELETE

            Args:
                request : 클라이언트로 부터의 요청

            Returns:
                output (json)   :  유저정보 수정 여부를 반환함.

            Raises:
                400 {"message" : "Bad request" } : 입력값이 잘못된 경우
                
                401  {"message": "unauthorization"} : 유저정보와 세션정보가 다를  경우

                405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
        """
    if request.method == 'PATCH':
        try:
            session_uid = check_session(request)
            if session_uid == 0:
                return JsonResponse({'message': 'session ID not found'}, status= 403)
            if user_uid == session_uid:  # 세션 유저와 url 상 유저가 동일.
                user = get_object_or_404(User, user_uid=user_uid)
                user_data = json.loads(request.body)

                user.user_email = user_data["user_email"]
                user.user_storename = user_data["user_storename"]
                user.set_password(user_data["user_pw"])
                user.save()
                output = {"message": "Ok"} ; CODE = 200
            else:  # 유저정보와 세션정보가 다를경우
                output = {"message": "unauthorization"}; CODE = 401
        except Exception as e:
            print(e)
            output = {"message": "bad input data"}; CODE = 400

    elif request.method == 'DELETE':
        output, CODE = delete_user(request, user_uid)

    else: # 허용하는 메소드가 아닐경우.
        output = {"message": "method not allowed"}; CODE = 405

    return JsonResponse(output, status=CODE)


# =============로그 아웃 함수==================

def logout(request):
    """
        유저 로그아웃 함수
            Allowed Method:
                    POST

            Args:
                request : 클라이언트로 부터의 요청

            Returns:
                output (json)   :  로그아웃 성공 여부를 반환함.

            Raises:
                400 {"message" : "not find session" } : 로그인 되어있지 않은 경우

                405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
        """
    if request.method == 'POST':
        try:
            auth.logout(request)
            output = {"message": "Ok"}; CODE = 200
        except Exception as e:
            print(e)
            output = {"message":  "not find session"};CODE = 401
    else :
        output = {"message": "method not allowed"}; CODE = 405

    return JsonResponse(output,status=CODE)

def dashboard(request) :    # 대시 보드 뷰
    """
            메인 화면 출력 함수
                Args:
                    request : 클라이언트로 부터의 요청

                Returns:
                    output (json)   :  비밀번호 변경 여부를 반환함.

                Raises:
                    400 {"message" : "Bad request" } : 입력값이 잘못된 경우

                    403{'message': 'session ID not found'} : 세션 아이디를 찾을 수 없는 경우

                    405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우
            """
    session_uid = check_session(request)
    if session_uid == 0:
        return JsonResponse({'message': 'session ID not found'}, status=403)

    if session_uid > 0:
        user_info = User.objects.filter(user_uid = request.session['auth']).prefetch_related('req_set')
        bill_data = Bill.objects.filter(user_uid=request.session['auth'],bill_date__range=[date.today() - timedelta(days=4), date.today()])

        med_data = Medicine.objects.filter(user_uid=request.session['auth'])
        emp_data = Employee.objects.filter(user_uid=request.session['auth'])
        com_data = Company.objects.filter(user_uid=request.session['auth'])

        output = main_data(user_info, bill_data, med_data, emp_data, com_data)

        return JsonResponse(output, status=200)