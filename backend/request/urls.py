from django.urls import path
from . import views
from bill.views import makeBill

urlpatterns = [
    path('bill', makeBill),
    path('req', views.postReq),
    path('req/<int:uid>', views.fixReq)
]
