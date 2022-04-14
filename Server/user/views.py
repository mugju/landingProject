from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
import json
from .models import User

from django.http import HttpResponse

# 로그인 함수
def signin(request):
    if request.method == "POST":
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email  = user_data["user_email"]
        user_password = user_data["user_pw"]
        # print("{},{}".format(user_email,user_password))
        user = authenticate(request, password=user_password, username=user_email)
        print(user)

        if user is None:    # 회원정보 없는 경우.
            result = "false"
        else:
            auth.login(request, user)
            result = "ok"
        output ={
            "message" : result
        }
    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

# 회원가입 함수
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
        
    else:  
        output = {"message" : "잘못된 접근."}
    
    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

# 패스워드 찾기 함수 ==> 회원정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
    user_data = json.loads(request.body)
    return "ok"

def pw_set(request):
    return "ok"

def edit_user(request):
    return "ok"

def delete_user(request):
    return "ok"