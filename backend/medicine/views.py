from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseBadRequest , JsonResponse
from django.db.models import Count,Prefetch
from django.core.paginator import Paginator

import json
from .models import Medicine , Med_salt
from user.models import User
from company.models import Company

#세션에 담긴 uid가 User에 존재하는지 확인
def medSession(request):
    try:
        sessionId = request.session['auth'] #세션에 아이디가 있는지 없는지 확인
    except:# except에 들어오게 되면 session에 ID가 존재하지 않는것이다.
        return 403
    try:
       userAuth = get_object_or_404(User, user_uid = sessionId)#세션아이디가 회원인지 확인
       return userAuth.user_uid
    except User.DoesNotExist:
       return 404

def med_index(request):
    user_uid = medSession(request) #권한 없음 404 에러 발생
    if user_uid == 403:
        return JsonResponse({'message':'session ID not found'}, status=403)
    elif user_uid == 404:
        return JsonResponse({'message': 'user not found'}, status =404)
    else:
        if request.method == 'GET':
            try:
                page = request.GET['page']
                if page !=1 :
                    start = ((int(page)*10)-10)
                    end = (int(page)*10)
                medicineLi = Medicine.objects.filter(user_uid=user_uid).prefetch_related('med_salt_set')
                medicineAllCount = medicineLi.count()#약의 개수 count
                medicinePage = list(medicineLi)[start:end]#페이징 개수만큼 잘라주기

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

#medicine insert 함수
def med_insert(request, user_uid):
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
    #새로 insert한 medcine의 med_uid 가져오기
    makeMeduid=Medicine.objects.get(user_uid=user_uid,med_name=med["med_name"]).med_uid
    #salt 추가 함수
    message = saltSave(med["med_salt"],makeMeduid)
    if message ==400: #slat 수정 실패 bad input data 일때
        return 400
    else:
        return "ok"

def med_detail(request, med_uid):
    #사용자 아이디 확인
    user_uid = medSession(request) #권한 없음 404 에러 발생
    if request.method == 'PATCH':
        try:
            #medicine 정보 수정
            message = editMedicine(request, med_uid, user_uid)
            if message == 400:
                context = {'message':'bad input data'}
                status = 400
            elif message ==401:
                context = {'message':'unauthorized'}
                status = 401
            else:
                context = {'message': message}
                status =200
            return JsonResponse(context, json_dumps_params={'ensure_ascii': False} , status = status)
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

    #해당 med_uid의 salt를 다 지워버리자
    Med_salt.objects.filter(med_uid=med_uid).delete()#해당하는 uid salt데이터 가져오고 지우기
    #med_salt inset, update함수
    result =saltSave(med_edit["med_salt"], med_uid)
    if result == 400:# salt update 중에 bad input 있을때
        return 400
    else:
        return "ok"


#salt detail insert&update 함수
def saltSave(salt_arr, med_uid):
    try:
        for salt in salt_arr:
            med_salt = Med_salt(
                med_uid=Medicine.objects.get(pk=med_uid),
                salt_name=salt["salt_name"],
                salt_qty=salt["salt_qty"],
                salt_qty_type=salt["salt_qty_type"],
                salt_desc=salt["salt_desc"]
                )
            med_salt.save()
        return "ok"
    except:
        return 400
#         else: #salt update (edit)
#             print("update if문")
#             med_salt = Med_salt(salt_uid=salt["salt_uid"],
#                             med_uid=Medicine.objects.get(pk=med_uid),
#                             salt_name=salt["salt_name"],
#                             salt_qty=salt["salt_qty"],
#                             salt_qty_type=salt["salt_qty_type"],
#                             salt_desc=salt["salt_desc"]
#                             )
#             med_salt.save()
            #push origin default로 되는가