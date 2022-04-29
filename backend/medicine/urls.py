from django.urls import path

from . import views

urlpatterns = [
    path('', views.med_index),
    path('<int:med_uid>/',views.med_detail), #medlist 페이지에서 medname클릭시 detail페이지로 이동
]