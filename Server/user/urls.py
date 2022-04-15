from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin),
    path('signup/', views.signup),
    path('find/',views.pw_find),
    path('set/',views.pw_set),
    path('<int:user_uid>/', views.edit_user),



    path('signout/',views.signout)
]
