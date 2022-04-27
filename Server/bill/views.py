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
            return HttpResponseBadRequest(json.dumps('Bad request'))

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
            result = {'bill_total_sell':totalSell ,' bill_profit': totalProfit}
            Bill.objects.update_or_create(bill_date = inputdata.joindate ,
            defaults=result)

            return JsonResponse({'message': 'ok'},safe=False, status = 200)
        except: 
            return HttpResponseBadRequest(json.dumps('Bad request'))
    
    else:
        return HttpResponse(('Bad request'), status = 400)