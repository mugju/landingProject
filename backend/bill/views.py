from django.db.models import Subquery, OuterRef
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
    """
    Bill GET, POST 함수        
        Allowed Method:
            GET  
            POST

        Returns:
            GET(int): User가 작성한 Medicine의 전체 내역에서 {'med_uid', 'med_name', 'med_sellprice'} 데이터만 반환한다.
            POST: bill이 정상적으로 저장되면 {message: ok}를 반환합니다.

        Raises:
            400 {"message" : "not find session" } : 로그인 되어있지 않은 경우 

            401 {"message" : "unauthorized" } : 권한없는 게시물에 접근할 경우      

            403 {"message" : "session ID not found"} : User의 권한이 없는경우

            404 {"message" : "user not found" } : 유저의 정보를 찾을 수 없는 경우
            
            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우    
    """
    if request.method == 'GET':
        userAuth = checkAuth(request)
        if type(userAuth) == JsonResponse:
            return userAuth

        try:
            medList = list(Medicine.objects.filter(user_uid = userAuth.user_uid) \
                           .values('med_uid', 'med_name', 'med_sellprice'))
            return JsonResponse(medList, safe=False, status=200)
        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    elif request.method == 'POST':
        userAuth = checkAuth(request)
        if type(userAuth) == JsonResponse:
            return userAuth

        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            totalProfit = 0
            totalSell = 0
            medArr = []
            amountList = {}

            for i in inputdata['med_list']:
                medArr.append(i['med_uid'])
                #[{1:20}, {2:30}]
                amountList[i['med_uid']] = i['detail_amount']
                
            #각 medicien의 정보를 받옴 
            medData = Medicine.objects.filter(med_uid__in=medArr).values('med_uid', 'med_buyprice', 'med_sellprice')
            if len(medData) == 0:
                return JsonResponse({'message': 'unauthorized'}, status=401)
            #[{med_uid:1 , med_buyPrice: 100 , med_sellPrice: 300}]
            for i in medData:
                i['med_profit'] = (i['med_buyprice'] - i['med_sellprice'])
                #[{med_uid:1 , med_buyPrice: 100 , med_sellPrice: 300, med_profit: 200}]
                totalProfit += amountList[i['med_uid']] * i['med_profit']
                totalSell += amountList[i['med_uid']] * i['med_sellprice']
                
            try: 
                checkBill = Bill.objects.get(user_uid=userAuth.user_uid,bill_date = inputdata['joindate'])
                print(checkBill.bill_date)
                saveSell = checkBill.bill_total_sell
                saveProfit = checkBill.bill_profit
            except Bill.DoesNotExist: 
                saveSell = 0
                saveProfit = 0
            except:
                return JsonResponse({'message': 'unauthorized'}, status=401)
                
            result = {'bill_total_sell':totalSell+ saveSell ,'bill_profit': totalProfit+saveProfit, 'user_uid': userAuth}
            Bill.objects.update_or_create(bill_date = inputdata['joindate'],defaults = result ,)
            return JsonResponse({'message': 'ok'}, safe=False, status=200)
            
        except Medicine.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'}, status=401)

        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)
