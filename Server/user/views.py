from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
import json
from .models import User

from django.http import HttpResponse

# ==============로그인 함수=================
def signin(request):
    if request.method == "POST":
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email  = user_data["user_email"]
        user_password = user_data["user_pw"]

        user = authenticate(request, password=user_password, username=user_email) # 유저 인증과정

        request.session['user_uid'] = user.user_uid # 세션을 통해 uid 넘겨줌

        if user is None:    # 회원정보 없는 경우.
            result = "회원정보 없음."
        else:
            auth.login(request, user)
            result = "ok"
        output ={
            "session_uid" : request.session.get('user_uid'),
            "message" : result
        }
    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

# ===============회원가입 함수===============
def signup(request):
    if request.method=='POST':
        print("회원가입 로직")
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 회원가입 정보.

        if user_data["user_pw"] == user_data["user_pw_confirm"]:     # 비밀번호 확인
            user = User.objects.create_user(
                user_email = user_data["user_email"],
                password = user_data["user_pw"],
                user_storename = user_data["user_storename"]
            )
            auth.login(request, user)
            output = {"message": "장고 기본 테이블에 회원가입 진행."}

        else:
            output = {"message": "비밀번호 확인 실패."}
        
    else:  # post 이외 방식
        output = {"message" : "잘못된 접근."}
    
    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

# 패스워드 찾기 함수 ==> 회원정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
    if request.method=='POST':
        user_data = json.loads(request.body)

        try: # 입력정보 기반 db에서 회원정보 탐색.
            user = User.objects.get(user_email=user_data["user_email"])
            print(user.user_storename)
            if user.user_storename == user_data["user_storename"]:
                output = {"message": "회원정보 일치, 비밀번호 리셋으로 리다이렉트"}
            else:
                output = {"message": "회원정보 불일치, 얼럿메시지 발행"}
        except :
            output = {"message": "해당 회원정보 없음.!!"}


        return HttpResponse(json.dumps(output),
                            content_type=u"application/json; charset=utf-8",
                            status=200)

def pw_set(request):
    return "ok"

def edit_user(request):
    return "ok"

def delete_user(request):
    return "ok"