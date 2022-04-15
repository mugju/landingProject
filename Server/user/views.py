from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
import json
from .models import User

from django.http import HttpResponse


# ==============로그인 함수=================
def signin(request):
    if request.method == "POST":
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email = user_data["user_email"]
        user_password = user_data["user_pw"]

        user = authenticate(request, password=user_password, username=user_email)  # 유저 인증과정

        if user is None:  # 회원정보 없는 경우.
            result = "회원정보 없음."
            print(user)
        else:
            auth.login(request, user)
            result = "ok"
            request.session['user_uid'] = user.user_uid  # 세션을 통해 uid 넘겨줌
        output = {
            "user_uid": request.session.get('user_uid'),
            "message": result
        }
    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


# ===============회원가입 함수===============
def signup(request):
    if request.method == 'POST':
        print("회원가입 로직")
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 회원가입 정보.

        if user_data["user_pw"] == user_data["user_pw_confirm"]:  # 비밀번호 확인
            user = User.objects.create_user(
                user_email=user_data["user_email"],
                password=user_data["user_pw"],
                user_storename=user_data["user_storename"]
            )
            auth.login(request, user)
            output = {"message": "장고 기본 테이블에 회원가입 진행."}

        else:
            output = {"message": "비밀번호 확인 실패."}

    else:  # post 이외 방식
        output = {"message": "잘못된 접근."}

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


# 패스워드 찾기 함수 ==> 회원정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)

        try:  # 입력정보 기반 db에서 회원정보 탐색.
            user = User.objects.get(user_email=user_data["user_email"])
            print(user.user_storename)
            if user.user_storename == user_data["user_storename"]:
                request.session['user_uid'] = user.user_uid
                output = {
                    "message": "회원정보 일치, 비밀번호 리셋으로 리다이렉트",
                    "user_uid": request.session["user_uid"]
                }

            else:
                output = {"message": "회원정보 불일치, 얼럿메시지 발행"}
        except:
            output = {"message": "해당 회원정보 없음.!!"}

        return HttpResponse(json.dumps(output, ensure_ascii=False),
                            content_type=u"application/json; charset=utf-8",
                            status=200)


def pw_set(request):
    if request.method == 'POST':
        try:
            user_uid = request.session["user_uid"]
            print(user_uid)
            output = {"message": "회원정보 있음."}
            user = User.objects.get(user_uid=user_uid)
            new_pw = json.loads(request.body)["user_new_pw"]
            print("new pw : {}".format(new_pw))
            user.set_password(new_pw)
            user.save()


        except:
            output = {"message": "회원정보 없음, 얼럿메시지 발행"}

    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

def delete_user(request,user_uid): # 슈퍼유저 혹은 본인이어야 회원 탈퇴 가능
    user_uid_s = request.session["user_uid"]
    user = User.objects.get(user_uid = user_uid_s)

    if user.is_superuser == 1 or user.user_uid == user_uid:
        delete_user = User.objects.get(user_uid = user_uid)
        delete_user.delete()
        return {"message": "유저정보 삭제"}
    else:
        return {"message"  : "삭제 권한이 없는 유저입니다."}

def edit_user(request,user_uid):
    if request.method == 'PATCH':
        try:
            user_uid_s = request.session["user_uid"]
            if user_uid == user_uid_s: # 세션 유저와 url상 유저가 동일.
                user = User.objects.get(user_uid=user_uid)
                user_data = json.loads(request.body)
                user.user_email = user_data["user_email"]
                user.user_storename = user_data["user_storename"]
                user.save()
                output = {"message": "유저정보 수정"}
            else:
                output = {"message": "세션 유저와 수정대상 유저가 동일하지 않습니다."}
        except:
            output = {"message": "세션내 유저정보가 없습니다."}

    elif request.method=='DELETE':
        output = delete_user(request,user_uid)

    else :
        output = {"message": "잘못된 접근 ."}

    return HttpResponse(json.dumps(output, ensure_ascii=False),
                            content_type=u"application/json; charset=utf-8",
                            status=200)



def signout(request):
    auth.logout(request)
    output = {"message": "로그아웃"}
    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=200)
