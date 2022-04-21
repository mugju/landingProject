from django.urls import path
from . import views


urlpatterns = [
    path('', views.companyMain),
    path('<int:uid>', views.companyDetail)
]