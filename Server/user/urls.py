from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin),       # 로그인
    path('signup/', views.signup),      # 회원 가입
    path('find/',views.pw_find),        #  회원정보 찾기
    path('set/',views.pw_set),      #회원 비밀번호 변경
    path('<int:user_uid>/', views.edit_user),      # 회원정보 변경 및 삭제



    path('logout/',views.logout),      # 로그아웃

]
