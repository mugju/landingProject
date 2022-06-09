from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseBadRequest , JsonResponse
from django.db.models import Count,Prefetch
from django.core.paginator import Paginator

import json
from .models import Medicine , Med_salt
from user.models import User
from company.models import Company


#DB에서 진짜 캐싱을 하는지 확인하기 위한 datetime
from datetime import datetime

#세션에 담긴 uid가 User에 존재하는지 확인
def medSession(request):
    """세션 uid 확인함수
        Args:
            request: 클라이언트로 부터의 요청

        Returns:
            output: 클라이언트의 user_uid를 반환함

        Raises:
            403{"message":'session ID not found'} : session에 ID가 존재하지 않은 경우
            404{'message': 'user not found'} : 존재하지 않는 유저인 경우

        Note:
            med_index, med_detail 함수 도입부에 현재 함수를 통해 유저의 session id를 확인한다.
    """
    try:
        sessionId = request.session['auth'] #세션에 아이디가 있는지 없는지 확인
    except:# except에 들어오게 되면 session에 ID가 존재하지 않는것이다.
        return JsonResponse({'message':'session ID not found'}, status=403)
    try:
       userAuth = get_object_or_404(User, user_uid = sessionId)#세션아이디가 회원인지 확인
       return userAuth.user_uid
    except User.DoesNotExist:
       return JsonResponse({'message': 'user not found'}, status =404)

def med_index(request):
    """GET, POST 방식의 medicine 페이지 접근함수
        Allowed Method:
            GET, POST
        Args:
            request: 클라이언트로 부터의 요청

        Returns:
            output(json):
                GET 방식: 약품수, 약품 list, 회사 list
                POST 방식: medicine 수정 여부

        Raises:
            400{'message':'bad input data'}: medicine의 형식에 맞지 않는 데이터를 넣었을 때
            405{'message': 'method not allowed'}: GET,POST 가 아닌 방식으로 함수에 접근했을 때때

    """
    uer_uid = medSession(request)
    if type(user_uid) == JsonResponse:# session 확인 함수에서 error 발생시
        return user_uid
    else:
        if request.method == 'GET':
            try:
                page = request.GET['page']
                if page !=1 :
                    start = ((int(page)*10)-10)
                    end = (int(page)*10)

                medicineLi = list(Medicine.objects.filter(user_uid=user_uid).prefetch_related('med_salt_set'))#미리 데이터를 캐싱하기 위해 list로 바로 DB에 접근
                medicineAllCount = len(medicineLi)#전체 약의 개수
                medicinePage = medicineLi[start:end]#페이징 개수만큼 잘라주기

                companyLi = list(Company.objects.filter(user_uid=user_uid).order_by('com_uid')) #user의 거래처 uid, 이름 list
                company_list = []
                i = 1 #company_list 앞에 uid가 아닌 순서를 넣기 위해
                for data in companyLi:
                    company_list.append({str(i) : data.com_name})
                    i=i+1

                medicine_list = []
                for data in medicinePage:
                    new = {}
                    new['med_uid'] = data.med_uid
                    new['med_name'] = data.med_name
                    new['med_type'] = data.med_type
                    new['med_buyprice'] = data.med_buyprice
                    new['med_sellprice'] = data.med_sellprice
                    new['med_cgst'] = data.med_cgst
                    new['med_sgst'] = data.med_sgst
                    new['med_expire'] = data.med_expire.strftime('%Y-%m-%d')
                    new['med_mfg'] = data.med_mfg.strftime('%Y-%m-%d')
                    new['med_desc'] = data.med_desc
                    new['med_instock'] = data.med_instock
                    new['med_qty'] = str(data.med_qty)
                    new['med_company'] = data.med_company
                    new['med_salt'] = list(data.med_salt_set.values("salt_uid", "salt_name", "salt_qty", "salt_qty_type", "salt_desc"))
                    medicine_list.append(new)
                context = {'medicineallcount':medicineAllCount, 'medicine_list': medicine_list, 'company_list': company_list}
                return JsonResponse(context, json_dumps_params={'ensure_ascii': False} , status = 200)
            except Exception as e:
                return JsonResponse({'Exception': e})
        elif request.method == 'POST':#POST 방식일때
            try:
                message = med_insert(request, user_uid)
                if message == 400: #medicine 수정 실패 bad input data 일때
                    context = {'message':'bad input data'}
                    status = 400
                else:
                    context = {"message" : message}
                    status = 200
                return JsonResponse(context, json_dumps_params={'ensure_ascii': False} , status = status)
            except:
                return HttpResponseBadRequest(json.dumps('Bad request'))
        else:# GET,POST가 아닐때
            return JsonResponse({'message': 'method not allowed'}, status =405)

def med_insert(request, user_uid):
    """medicine 추가 함수
        Args:
            request: 클라이언트의 요청
            user_uid: session에 있는 유저의 ID

        Returns:
            output : medicine 추가 성공 여부

        Raises:
            400 : 추가 실패 error 코드

    """
    med = json.loads(request.body) #JSON data parsing
    try:
        medAdd = Medicine(user_uid=User.objects.get(user_uid = request.session['auth']),
            med_name = med["med_name"],
            med_type = med["med_type"],
            med_buyprice= med["med_buyprice"],
            med_sellprice= med["med_sellprice"],
            med_cgst= med["med_cgst"],
            med_sgst= med["med_sgst"],
            med_expire= med["med_expire"],
            med_mfg= med["med_mfg"],
            med_desc= med["med_desc"],
            med_instock= med["med_instock"],
            med_qty= med["med_qty"],
            med_company= med["med_company"])
        medAdd.save()
    except:
        return 400
    if not med["med_salt"]:
        #salt가 비어있으면 끝내기
        return "ok"
    else:#salt가 존재
        message = saltSave(med["med_salt"],makeMeduid)
        if message ==400: #slat 수정 실패 bad input data 일때
            return 400
        else:
            return "ok"

def med_detail(request, med_uid):
"""PATCH, DELETE 방식의 medicine 페이지 접근함수
    Allowed Method: PATCH, DELETE

    Args:
        request : 클라이언트의 요청
        med_uid : 약품 유효번호

    Returns:
        output(json) :
            PATCH 방식: medicine 수정 성공 여부
            DELETE 방식: delete 성공 여부

    Raises:
        400{'message':'bad input data'}: 수정할 데이터의 값이 유효하지 않을때
        401{'message':'unauthorized'}: 수정, 삭제 요청자가 권한이 없을때
        405{'message': 'method not allowed'}: PATCH, DELETE 가 아닌 다른 method 로 요청 했을때

    Note:
        여기서 발생하는 400,401error는 try문으로 발생하는 error가 아니라 editMedicine을 통해 발생한
        error값이 return 되어 발생하는 것이다.
"""
    #사용자 아이디 확인
    user_uid = medSession(request)
    if type(user_uid) == JsonResponse:# session 확인 함수에서 error 발생시
        return user_uid
    else: #사용자 아이디 확인 후 수정, 삭제 할 수 있다.
        if request.method == 'PATCH':
            try:
                #medicine 정보 수정
                message = editMedicine(request, med_uid, user_uid)
                if message == 400:
                    return JsonResponse({'message':'bad input data'}, json_dumps_params={'ensure_ascii': False} , status = 400)
                elif message ==401:
                    return JsonResponse({'message':'unauthorized'}, json_dumps_params={'ensure_ascii': False} , status = 401)
                else:
                    return JsonResponse({'message': message}, json_dumps_params={'ensure_ascii': False} , status = 200)
            except:
                return HttpResponseBadRequest(json.dumps('Bad request'))
        elif request.method == 'DELETE':
            try:
                medDelData = Medicine.objects.get(med_uid=med_uid)
            except: #삭제할 med_uid를 조회했을때 badinput data이면 권한 없는게 맞다.
                return JsonResponse({'message': 'bad inpu data'}, json_dumps_params={'ensure_ascii': False} , status = 400)

            if medDelData.user_uid_id != user_uid:# medcine_uid와 user_uid가 다르면 권한이 없다.
                return JsonResponse({'message': 'unauthorized'}, json_dumps_params={'ensure_ascii': False} , status = 401)
            else:#권한 있으면 삭제
                medDelData.delete()
                return JsonResponse({"message":"ok"}, json_dumps_params={'ensure_ascii': False} , status = 200)
        else:# PATCH,DELETE가 아닐때
            return JsonResponse({'message': 'method not allowed'}, status =405)

#med_detail edit 함수
def editMedicine(request, med_uid, user_uid):
    """medicine 수정 함수
        Args:
            request: 클라이언트 요청
            med_uid: 수정하는 medicine 유효번호
            user_uid: 수정하려는 클라이언트이 user_uid

        Returns:
            nomal return: medicine 수정 여부 알려주는 메세지

        Raises:
            401: 존재하지 않는 medicine의 값을 변경하려고 했을 때, session의 user_uid와 medicine을 등록한 user_uid가 다를때
            400: medicine 수정 데이터가 유효하지 않을때

        Notes:
            이 함수에서 error가 발생하면 except로 error코드를 return 하여 med_detail함수에서 error 처리를 해준다.
    """
    med_edit = json.loads(request.body) #JSON data parsing
    try:
        medicine = Medicine.objects.get(med_uid=med_uid)
    except: #존재하지 않는 uid를 조회해도 권한 없는 요청 401error 발생
        return 401

    if medicine.user_uid_id != user_uid: #session의 uid와 변경하려면 uid가 같지 않다면 권한 없는 요청 401 error발생
        return 401
    try:
        medicine.med_name = med_edit["med_name"]
        medicine.med_type = med_edit["med_type"]
        medicine.med_buyprice= med_edit["med_buyprice"]
        medicine.med_sellprice= med_edit["med_sellprice"]
        medicine.med_cgst= med_edit["med_cgst"]
        medicine.med_sgst= med_edit["med_sgst"]
        medicine.med_expire= med_edit["med_expire"]
        medicine.med_mfg= med_edit["med_mfg"]
        medicine.med_desc= med_edit["med_desc"]
        medicine.med_instock= med_edit["med_instock"]
        medicine.med_qty= med_edit["med_qty"]
        medicine.med_company= med_edit["med_company"]
        medicine.save()
    except:
        return 400
    #일단 수정할 med_salt가 있는지 확인을 하고 있으면 salt부분 만져주고 아니면 return "ok"하기
    if not med_edit["med_salt"]:
        #salt가 비어있으면 끝내기
        return "ok"
    else:
        #해당 med_uid의 salt를 다 지워버리자
        pre_med_salt = list(Med_salt.objects.filter(med_uid=med_uid)) #error를 대비해 미리 저장해놓기
        Med_salt.objects.filter(med_uid=med_uid).delete()#해당하는 uid salt데이터 가져오고 지우기
        #med_salt inset, update함수
        result = saltSave(med_edit["med_salt"], medicine)
        if result == 400:# salt update 중에 bad input 있을때
            saltSave(pre_med_salt,med_uid)#지운 salt 정보 다시 저장하기
            return 400
        else:
            return "ok"


#salt detail insert&update 함수
def saltSave(salt_arr, med):
    """medicine의 salt목록 insert, update 함수
        Args:
            salt_arr: insert및 update할 medicine의 salt list
            med: insert및 update할 medicine의 Model, med_uid를 위해 필요하다.

        Returns:
            output: salt insert, update 성공 여부

        Raises:
            400: salt insert, update 실패할 시,(salt에 데이터에 유효하지 않은 데이터가 있을경우 발생생) 400 error return한다.

    """
    try:
        for salt in salt_arr:
            med_salt = Med_salt(
                med_uid=med,
                salt_name=salt["salt_name"],
                salt_qty=salt["salt_qty"],
                salt_qty_type=salt["salt_qty_type"],
                salt_desc=salt["salt_desc"]
                )
            med_salt.save()
        return "ok"
    except:
        return 400