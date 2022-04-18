from django.db.models import Subquery , OuterRef
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse
from django.utils.dateformat import DateFormat

import json
from datetime import datetime 

from company.views import checkAuth
from bill.models import Bill, Bill_detail
from medicine.models import Medicine
from user.models import User


def makeBill(request):
    if request.method == 'GET': 
        userAuth = checkAuth(request.headers)
        try:
            medList = list(Medicine.objects.all()\
                .values('med_uid', 'med_name', 'med_sellprice'))
            return JsonResponse(medList,safe=False, status = 200)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

    elif request.method == 'POST':
        userAuth = checkAuth(request.headers)
        try:
            inputdata = json.loads(request.body.decode('utf-8'))

            totalProfit = 0
            totalSell = 0
            amountList = {}
            medNamelist = []
            detailarr = []

            for i in inputdata['bill_detail']:
                medNamelist.append(i['detail_med_name'])
                amountList[i['detail_med_name']]  = i['detail_amount']
            
            medPrice = Medicine.objects.filter(med_name__in = medNamelist)\
                .values('med_uid', 'med_name', 'med_buyprice', 'med_sellprice')

            for i in medPrice:
                i['med_profit'] = (i['med_buyprice'] - i['med_sellprice'])  
                totalProfit += amountList[i['med_name']] * i['med_profit']
                totalSell += amountList[i['med_name']] * i['med_sellprice']        
            
            datenow = DateFormat(datetime.now()).format('Y-m-d')

            inputBill = Bill.objects.create(
                user_uid = userAuth,
                bill_customer_name = inputdata['bill_customer_name'],
                bill_address = inputdata['bill_address'],
                bill_phone = inputdata['bill_phone'],
                bill_id = inputdata['bill_id'],
                bill_total_sell = totalSell,
                bill_profit = totalProfit,
                bill_date = datenow
            )

            for i in inputdata['bill_detail']:
                detailarr.append(Bill_detail(detail_sr_no = 1 , detail_med_name = i['detail_med_name'] ,
                detail_qty = i['detail_qty'] , detail_qty_type = i['detail_qty_type'] 
                , detail_unit_price = i['detail_unit_price'] , detail_amount = i['detail_amount'] , bill_uid = inputBill ))
            
            Bill_detail.objects.bulk_create(detailarr)

            return JsonResponse({'message': 'ok'},safe=False, status = 200)
        except: 
            return HttpResponseBadRequest(json.dumps('Bad request'))