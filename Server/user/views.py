from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate
import json
from .models import User

from django.http import HttpResponse


# ==============로그인 함수=================
def signin(request):
    if request.method == "POST":    # 정상적인 접근
        user_data = json.loads(request.body)  # JSON data parsing / 여기에선 로그인 정보.
        user_email = user_data["user_email"]
        user_password = user_data["user_pw"]

        user = authenticate(request, password=user_password, username=user_email)  # 유저 인증과정

        if user is None:  # 회원정보 없는 경우.
            return HttpResponse(json.dumps({"message" : "Bad request" }),
                                content_type=u"application/json; charset=utf-8",
                                status=200)
        else:
            auth.login(request, user)
            request.session['user_uid'] = user.user_uid  # 세션을 통해 uid 넘겨줌

            # user_info = User.objects.get(user_uid = request.session.get('user_uid'))
            user_info = get_object_or_404(User, user_uid = request.session.get('user_uid') )
        output = {      # 여기 값이 달라져야함.
            "user_uid": user_info.user_uid,
            "user_storename": user_info.user_storename,
            # API대로 추가 정보 넘겨야 함.
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
            output = {"message": "ok"}

        else:   # 비밀 번호가 같지 않은 경우.
            output = {"message": "Password authorization failed"}

    else:  # post 이외 방식 으로 접근 한 경우.
        output = {"message": "Bad request"}

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


# 패스워드 찾기 함수 ==> 회원정보를 찾아 json으로 ok 응답 넘김.
def pw_find(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)

        # 입력정보 기반 db에서 회원정보 탐색.
        user = get_object_or_404(User, user_email = user_data["user_email"] )

        if user.user_storename == user_data["user_storename"]:
            request.session['user_uid'] = user.user_uid
            output = {
                "message": "ok",
                # "user_uid": request.session["user_uid"]
            }

        else:
            output = {"message": "Incorrect user storename"}

    else:
        output = {"message": "Bad request"}

    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


def pw_set(request):
    if request.method == 'POST':
        try:
            user_uid = request.session["user_uid"]
            user = get_object_or_404(User, user_uid = user_uid)
            new_pw = json.loads(request.body)["user_new_pw"]

            user.set_password(new_pw)
            user.save()
            output = {"message": "Ok"}
        except:
            output = {"message": "Bad request"}

    return HttpResponse(json.dumps(output),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


def delete_user(request,user_uid): # 슈퍼유저 혹은 본인이어야 회원 탈퇴 가능
    session_uid = request.session["user_uid"]
    user = get_object_or_404(User, user_uid=session_uid)

    if user.is_superuser == 1 or user.user_uid == user_uid:     # 어드민 이거나, 본인일 경우에 삭제 가능.
        delete_user = User.objects.get(user_uid = user_uid)
        delete_user.delete()
        return {"message": "Ok"}
    else:
        return {"message"  : "Permission rejected"}


def edit_user(request,user_uid):
    if request.method == 'PATCH':
        try:
            session_uid = request.session["user_uid"]
            if user_uid == session_uid: # 세션 유저와 url상 유저가 동일.
                user = get_object_or_404(User, user_uid=user_uid)
                user_data = json.loads(request.body)

                user.user_email = user_data["user_email"]
                user.user_storename = user_data["user_storename"]
                user.save()
                output = {"message": "Ok"}
            else:
                output = {"message": "Permission denied"}
        except:
            output = {"message": "Bad request"}

    elif request.method=='DELETE':
        output = delete_user(request,user_uid)

    else :
        output = {"message": "Bad request"}

    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=200)


def logout(request):
    auth.logout(request)
    output = {"message": "Ok"}
    return HttpResponse(json.dumps(output, ensure_ascii=False),
                        content_type=u"application/json; charset=utf-8",
                        status=200)

