from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
import json

from django.http import HttpResponse

# Create your views here.
def login(request):
    if request.method == "POST":
        print("test")
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email  = user_data["user_email"]
        user_password = user_data["user_pw"]
        print("{},{}".format(user_email,user_password))
        user = authenticate(request, password=user_password, username=user_email)
        print(user)

        output = "유저 정보 날려야함."
    return HttpResponse(output,
                        content_type=u"application/json; charset=utf-8",
                        status=200)

def signin(request):
    if request.method=='POST':
        print("회원가입 로직")
        output = "장고 기본 테이블에 회원가입 진행."
    return HttpResponse(output,
                        content_type=u"application/json; charset=utf-8",
                        status=200)


def pw_find(request):
    return "ok"

def pw_set(request):
    return "ok"

def edit_user(request):
    return "ok"

def delete_user(request):
    return "ok"