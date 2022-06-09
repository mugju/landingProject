from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json

from company.views import checkAuth
from user.models import User
from request.models import Cus_req


def postReq(request):
    """
    Request GET, POST 함수        
        Allowed Method:
            GET  
            POST
            
        Args:
            request : 클라이언트의 요청 

        Returns:
            GET(int): User가 작성한 Request내역을 int로 페이징하여 반환합니다.
            POST: 정상적으로 게시글이 작성되면 {message: ok}를 반환합니다.

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
            page = request.GET['page'] 
            if int(page) >= 1:
                start = ((int(page) * 10) - 10)
                end = (int(page) * 10)
                #잘못된 값이 query로 들어올경우의 예외처리 
            else:return JsonResponse({'message': 'bad input data'}, status= 400)

            targetdata = Cus_req.objects.filter(user_uid = userAuth.user_uid)\
                .values('req_uid', 'req_name','req_phone', 'req_med_detail' , 'req_joindate' , 'req_status')
            targetresult = list(targetdata[start:end])
            targetcount = targetdata.count()

            return JsonResponse({'requestallcount':targetcount,'request_list':targetresult},safe=False, status = 200)
        except:
            return JsonResponse({'message': 'bad input data'},safe=False, status = 400)

    if request.method == 'POST':
        userAuth = checkAuth(request)
        if type(userAuth) == JsonResponse:
            return userAuth

        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            Cus_req.objects.create(
                req_name=inputdata['req_name'],
                req_phone=inputdata['req_phone'],
                req_med_detail=inputdata['req_med_detail'],
                req_joindate=inputdata['req_joindate'],
                req_status=False,
                user_uid=userAuth
            )

            return JsonResponse({'message': 'ok'}, safe=False, status=200)

        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)


def fixReq(request, uid):
    """
    Request PATCH, DELETE 함수       
        Allowed Method:
            PATCH
            DELETE
            
        Args
            request : 클라이언트의 요청
            uid : Target Request 번호
            

        Returns:
            PATCH(int): int를 uid로 가지는 Request status를 수정합니다.
            DELETE: Request게시글을 삭제합니다.

        Raises:
            400 {"message" : "not find session" } : 로그인 되어있지 않은 경우     

            401 {"message" : "unauthorized" } : 권한없는 게시물에 접근할 경우      

            403 {"message" : "session ID not found"} : User의 권한이 없는경우

            404 {"message" : "user not found" } : 유저의 정보를 찾을 수 없는 경우

            405 {"message" : "method not allowed"} :  잘못된 method 요청이 들어온 경우    
    """
    if request.method == 'PATCH':
        userAuth = checkAuth(request)
        if type(userAuth) == JsonResponse:
            return userAuth

        try:
            targetInfo = Cus_req.objects.get(user_uid=userAuth.user_uid, req_uid=uid)
            targetStatus = False
            targetStatus = True if targetInfo.req_status == False else targetStatus
            targetInfo.req_status = targetStatus
            targetInfo.save()
            return JsonResponse({'message': 'ok'}, safe=False, status=200)
        except Cus_req.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'}, safe=False, status=401)
        except:
            return JsonResponse({'message': 'bad input data'}, status=400)

    elif request.method == 'DELETE':
        userAuth = checkAuth(request)
        if type(userAuth) == JsonResponse:
            return userAuth
            
        try:
            targetInfo = Cus_req.objects.get(req_uid=uid, user_uid=userAuth.user_uid)  # userAuth.uid가 들어가야함
            targetInfo.delete()
            return JsonResponse({'message': 'Ok'}, status=200)

        except Cus_req.DoesNotExist:
            return JsonResponse({'message': 'unauthorized'}, safe=False, status=401)

        except:
            return JsonResponse({'message': 'bad input data'}, status=400)

    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)
