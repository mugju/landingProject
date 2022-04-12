from django.urls import path

from . import views

urlpatterns = [
    path('', views.med_index),
    path('<int:med_uid>/',views.med_detail), #medlist 페이지에서 medname클릭시 detail페이지로 이동
#     path('<int:med_uid>/salt_create/', views.salt_create)
    path('<int:med_uid>/salt_add/', views.salt_add),
]