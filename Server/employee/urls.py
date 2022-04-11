from django.urls import path
from . import views

urlpatterns = [
    path('', views.emp_index),
    path('<int:emp_uid>/', views.emp_detail)

]