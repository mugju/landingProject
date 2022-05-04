<<<<<<< HEAD:Server/request/views.py
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
            targetdata = list(Cus_req.objects.filter(user_uid = userAuth.user_uid)\
                .values('req_uid', 'req_name','req_phone', 'req_med_detail' , 'req_joindate' , 'req_status'))
            return JsonResponse(targetdata,safe=False, status = 200)
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
            targetInfo = Cus_req.objects.get(req_uid = uid, user_uid = 3) #userAuth.uid가 들어가야함    
            targetInfo.delete()
            return JsonResponse({'message': 'Ok'}, status = 200)

        except Cus_req.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'},safe=False, status = 401) 

        except:    
            return JsonResponse({'message': 'bad input data'}, status= 400) 

=======
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
            targetdata = list(Cus_req.objects.filter(user_uid = userAuth.user_uid)\
                .values('req_uid', 'req_name','req_phone', 'req_med_detail' , 'req_joindate' , 'req_status'))
            return JsonResponse(targetdata,safe=False, status = 200)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

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
            return HttpResponseBadRequest(json.dumps('Bad request'))

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
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

    elif request.method == 'DELETE':
        userAuth = checkAuth(request)
        try:
            targetInfo = Cus_req.objects.get(req_uid = uid, user_uid = 3) #userAuth.uid가 들어가야함    
            targetInfo.delete()
            return JsonResponse({'message': 'Ok'}, status = 200)

        except Cus_req.DoesNotExist:
            return HttpResponse(('Bad request'), status = 400)

        except:    
            return HttpResponse(('Bad request'), status = 400)    

>>>>>>> 1381d94efd18bdef3a2dc9ef23f024fd9d86d5ae:backend/request/views.py
