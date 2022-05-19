from os import curdir
from django.db.models import Subquery , OuterRef
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse
import json

from company.views import checkAuth
from user.models import User
from request.models import Cus_req


def postReq(request):
    if request.method == 'GET':
        userAuth = checkAuth(request)

        try:
            page = request.GET['page'] 
            if int(page) >= 1:
                start = ((int(page) * 10) - 10)
                end = (int(page) * 10)
                #잘못된 값이 query로 들어올경우의 예외처리 
            else:return JsonResponse({'message': 'bad input data'}, status= 400)

            targetdata = list(Cus_req.objects.filter(user_uid = userAuth.user_uid)\
                .values('req_uid', 'req_name','req_phone', 'req_med_detail' , 'req_joindate' , 'req_status'))
            targetcount = targetdata.count()
            targetresult = targetdata[start:end]
            return JsonResponse({'requestallcount':targetcount,'request_list':targetresult},safe=False, status = 200)
        except:
            return JsonResponse({'message': 'bad input data'},safe=False, status = 400)

    if request.method == 'POST':
        userAuth = checkAuth(request)
        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            
            Cus_req.objects.create(
                req_name = inputdata['req_name'],
                req_phone = inputdata['req_phone'],
                req_med_detail = inputdata['req_detail'],
                req_joindate = inputdata['req_joindate'],
                req_status = False,
                user_uid = userAuth
            )

            return JsonResponse({'message' : 'Ok'},safe=False, status = 200)

        except: 
            return JsonResponse({'message': 'bad input data'},safe=False, status = 400)
    
    else:
        return JsonResponse({'message': 'method not allowed'}, status= 405)

def fixReq(request, uid):
    if request.method == 'PATCH': 
        userAuth = checkAuth(request)
        try:
            targetInfo = Cus_req.objects.get(user_uid = userAuth.user_uid , req_uid = uid)
            targetStatus = False
            targetStatus = True if targetInfo.req_status == False else  targetStatus
            targetInfo.req_status = targetStatus
            targetInfo.save()
            return JsonResponse({'message' : 'Ok'},safe=False, status = 200)
        except Cus_req.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'},safe=False, status = 401) 
        except:
            return JsonResponse({'message': 'bad input data'}, status= 400) 

    elif request.method == 'DELETE':
        userAuth = checkAuth(request)
        try:
            targetInfo = Cus_req.objects.get(req_uid = uid, user_uid = userAuth.uid) 
            targetInfo.delete()
            return JsonResponse({'message': 'Ok'}, status = 200)

        except Cus_req.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'},safe=False, status = 401) 

        except:    
            return JsonResponse({'message': 'bad input data'}, status= 400) 

