from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate
import json
from .models import User
from bill.models import Bill
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse

# 날짜 관련
from datetime import date, timedelta, datetime


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates


from django.db.models import Sum


# ===============메인화면 관련 ======================

def main_data(user_data, bill_data):  # 로그인 및 회원가입시 메인화면에 나타내줄 데이터 셋
    output = dict()
    output["user_uid"] = user_data[0].user_uid
    output["user_storename"] = user_data[0].user_storename
    output["user_email"] = user_data[0].user_email
    output["user_totalreqs"] = user_data[0].req_set.filter(req_status=True).count()
    output["user_completedreq"] = user_data[0].req_set.filter(req_status=True).count()
    output["user_pendingreq"] = user_data[0].req_set.filter(req_status=False).count()

    profit_arr = list() # json 생성용
    sell_arr = list()

    for day in date_range(str(date.today() - timedelta(days=4)), str(date.today())):
        dic_profit = dict()
        dic_profit[str(day)] = bill_data.filter(bill_date=day).aggregate(Sum('bill_profit'))["bill_profit__sum"]
        profit_arr.append(dic_profit)
        
        dic_sell = dict()
        dic_sell[str(day)] = bill_data.filter(bill_date=day).aggregate(Sum('bill_total_sell'))["bill_total_sell__sum"]
        sell_arr.append(dic_sell)
    output['bill_profit'] = profit_arr
    output['bill_total_sell'] = sell_arr

    return output


# ==============로그인 함수=================
@method_decorator(csrf_exempt, name='dispatch')
def signin(request):
    if request.method == "POST":  # 정상적인 접근
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

            return HttpResponse(json.dumps({"message": "Bad request"}),
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

        user_info = User.objects.filter(user_uid=user.user_uid).prefetch_related('req_set')

        bill_data = Bill.objects.filter(user_uid=user.user_uid,
                                        bill_date__range=[date.today() - timedelta(days=4), date.today()])
        output = main_data(user_info, bill_data)

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


# ===============회원가입 함수===============
@method_decorator(csrf_exempt, name='dispatch')
def signup(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)  # JSON data parsing / 여기 에선 회원 가입 정보.

        # 이메일 중복된 경우
        email_confirm = User.objects.get(user_email = user_data["user_email"])
        if email_confirm is not None:
            return HttpResponse(json.dumps( {"email_duplicatied" : True}),
                                content_type=u"application/json; charset=utf-8",
                                status=400)

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
            output = main_data(user_info, bill_data)
            CODE = 200

        else:  # 비밀 번호가 같지 않은 경우.
            output = {"message": "Password authorization failed"}; CODE = 401

    else:  # post 이외 방식 으로 접근 한 경우.
        output = {"message": "Bad request"}; CODE = 400

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=CODE)


# 패스 워드 찾기 함수 ==> 회원 정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
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

    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json", status=CODE)


# =========패스 워드 재설정 ==> 유저 정보 찾은 이후에 가능함.===========

def pw_set(request):
    if request.method == 'POST':
        try:
            user_uid = request.session["auth"]
            user = get_object_or_404(User, user_uid=user_uid)
            new_pw = json.loads(request.body)["user_new_pw"]

            user.set_password(new_pw)
            user.save()
            output = {"message": "Ok"}; CODE = 200

        except Exception as e:
            print(e)
            output = {"message": "Bad request"}; CODE = 404

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=CODE)


# =================유저 삭제 함수================

def delete_user(request, user_uid):  # 슈퍼 유저 혹은 본인 이어야 회원 탈퇴 가능
    session_uid = request.session["auth"]
    user = get_object_or_404(User, user_uid=session_uid)

    if user.is_superuser == 1 or user.user_uid == session_uid:  # 어드민 이거나, 본인일 경우에 삭제 가능.
        User.objects.get(user_uid=user_uid).delete() # 찾아서 삭제함.
        return {"message": "Ok"}, 200
    else:
        return {"message": "unauthorized"}, 401


# ==============유저 정보 수정=====================

def edit_user(request, user_uid):
    if request.method == 'PATCH':
        try:
            session_uid = request.session["auth"]
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
    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=CODE)


# =============로그 아웃 함수==================

def logout(request):
    if request.method == 'POST':
        try:
            auth.logout(request)
            output = {"message": "Ok"}; CODE = 200
        except Exception as e:
            print(e)
            output = {"message": "user not found"};CODE = 404
    else :
        output = {"message": "method not allowed"}; CODE = 405
    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=CODE)
