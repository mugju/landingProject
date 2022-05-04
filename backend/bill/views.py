<<<<<<< HEAD
<<<<<<< HEAD:Server/bill/views.py
from django.db.models import Subquery , OuterRef
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse
from django.utils.dateformat import DateFormat

import json
from datetime import datetime 

from company.views import checkAuth
from bill.models import Bill
from medicine.models import Medicine
from user.models import User


def makeBill(request):
    if request.method == 'GET': 
        userAuth = checkAuth(request)
        try:
            medList = list(Medicine.objects.all()\
                .values('med_uid', 'med_name', 'med_sellprice'))
            return JsonResponse(medList,safe=False, status = 200)
        except:
            return JsonResponse({'message': 'bad input data'},safe=False, status = 400)

    elif request.method == 'POST':
        userAuth = checkAuth(request)
        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            totalProfit = 0
            totalSell = 0
            medArr = []
            amountList = {}

            for i in inputdata['med_list']:
                medArr.append(i['med_uid'])
                amountList[i['med_uid']] = i['detail_amount'] 

            medData = Medicine.objects.filter(med_uid__in = medArr).values('med_uid' ,'med_buyprice' ,'med_sellprice')

            for i in medData:
                i['med_profit'] = (i['med_buyprice'] - i['med_sellprice'])  
                totalProfit += amountList[i['med_uid']] * i['med_profit']
                totalSell += amountList[i['med_uid']] * i['med_sellprice']        
            result = {'bill_total_sell':totalSell ,' bill_profit': totalProfit, 'user_uid': userAuth}
<<<<<<< HEAD
            try:
                Bill.objects.update_or_create(bill_date = inputdata.joindate ,
                defaults=result)
            except:
                return JsonResponse({'message': 'unauthorized' }, status= 401)
=======
            
            Bill.objects.update_or_create(bill_date = inputdata.joindate ,
            defaults=result)
>>>>>>> c054e5d0d44682c33d279612184b0c4bb19af57d

            return JsonResponse({'message': 'ok'},safe=False, status = 200)
        except: 
            return JsonResponse({'message': 'bad input data'},safe=False, status = 400)
    
    else:
        return JsonResponse({'message': 'method not allowed'}, status= 405)
=======
from django.db.models import Subquery , OuterRef
=======
from django.db.models import Subquery, OuterRef
>>>>>>> f855597c9a195a9d1a39c91acbb3baa05d647688
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.dateformat import DateFormat

import json
from datetime import datetime

from company.views import checkAuth
from bill.models import Bill
from medicine.models import Medicine
from user.models import User


def makeBill(request):
    if request.method == 'GET':
        userAuth = checkAuth(request)
        try:
            medList = list(Medicine.objects.all() \
                           .values('med_uid', 'med_name', 'med_sellprice'))
            return JsonResponse(medList, safe=False, status=200)
        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    elif request.method == 'POST':
        userAuth = checkAuth(request)
        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            totalProfit = 0
            totalSell = 0
            medArr = []
            amountList = {}

            for i in inputdata['med_list']:
                medArr.append(i['med_uid'])
                amountList[i['med_uid']] = i['detail_amount']

            medData = Medicine.objects.filter(med_uid__in=medArr).values('med_uid', 'med_buyprice', 'med_sellprice')

            for i in medData:
                i['med_profit'] = (i['med_buyprice'] - i['med_sellprice'])
                totalProfit += amountList[i['med_uid']] * i['med_profit']
                totalSell += amountList[i['med_uid']] * i['med_sellprice']
            result = {'bill_total_sell': totalSell, ' bill_profit': totalProfit, 'user_uid': userAuth}
            try:
                Bill.objects.update_or_create(bill_date=inputdata.joindate,
                                              defaults=result)
            except:
                return JsonResponse({'message': 'unauthorized'}, status=401)

            return JsonResponse({'message': 'ok'}, safe=False, status=200)
        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    else:
<<<<<<< HEAD
        return HttpResponse(('Bad request'), status = 400)
>>>>>>> 1381d94efd18bdef3a2dc9ef23f024fd9d86d5ae:backend/bill/views.py
=======
        return JsonResponse({'message': 'method not allowed'}, status=405)
>>>>>>> f855597c9a195a9d1a39c91acbb3baa05d647688
