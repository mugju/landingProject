from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseBadRequest , JsonResponse
from django.db.models import Count,Prefetch
from django.core.paginator import Paginator

import json
from .models import Medicine , Med_salt
from user.models import User
from company.models import Company
# import time
#세션에 담긴 uid가 User에 존재하는지 확인
def medSession(request):
    try:
        headerAuth = request.session['auth']
        print('user uid 확인', headerAuth)
        userAuth = get_object_or_404(User, user_uid = headerAuth)
    except:
        return HttpResponse(json.dumps('Bad request'))
    finally:
        return userAuth

def med_index(request):
    #session 사용자 확인 불러야함
    if request.method == 'GET':
        user_uid=141 #테스트를 위해 임의로 해놓은것
        try:
#         아래 주석은 페이징 할때 쓰일 것
#             page = request.GET['page']
#             if page !=1 :
#                 start = ((int(page)*10)-10)
#                 end = (int(page)*10)
#             medicine_list = list(Medicine.objects.prefetch_related(Prefetch('med_uid', to_attr='med_salt.set()'))
#                                         .filter(user_uid=request.session['auth']))[start:end]

            medicineLi = Medicine.objects.filter(user_uid=user_uid).prefetch_related('med_salt_set')
            medicineAllCount = medicineLi.count()#약의 개수 count
#             medicinePage = list(medicineLi)[start:end]

            companyLi = Company.objects.filter(user_uid=user_uid) #user의 거래처 uid, 이름 list
            company_list = []
            for data in companyLi:
                company_list.append({data['com_uid'] : data['com_name']})

            medicine_list = []
            for data in medicineLi:
                new = {}
                new['med_uid'] = data.med_uid
                new['med_name'] = data.med_name
                new['med_type'] = data.med_type
                new['med_buyprice'] = data.med_buyprice
                new['med_sellprice'] = data.med_sellprice
                new['med_csgt'] = data.med_cgst
                new['med_sgst'] = data.med_sgst
                new['med_expire'] = str(data.med_expire)
                new['med_mfg'] = str(data.med_mfg)
                new['med_desc'] = data.med_desc
                new['med_instock'] = data.med_instock
                new['med_company'] = data.med_company
                new['med_salt'] = list(data.med_salt_set.values())
                print(data.med_salt_set.values())
                medicine_list.append(new)
            context = {'medicine_list': medicine_list, 'company_list': company_list, 'medicineallcount':medicineAllCount}
            return JsonResponse(context, json_dumps_params={'ensure_ascii': False} , status = 200)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))
    else:#POST 방식일때
        try:
            message = med_insert(request, user_uid)
            result = {"message" : message}
            return JsonResponse(result, json_dumps_params={'ensure_ascii': False} , status = 200)#  medicine add하고 어디로 보내줘야하지? get으로 다시 list 보내주어야하는것인가?
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

def med_detail(request, med_uid):
    #사용자 아이디 확인
    if request.method == 'PATCH':
        try:
            #medicine 정보 수정
            message = editMedicine(request, med_uid)
            result = {"message": message}
            return JsonResponse(result, json_dumps_params={'ensure_ascii': False} , status = 200)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))
    if request.method == 'DELETE':
        try:
            medDelDate = get_object_or_404(Medicine, med_uid=med_uid)
            medDelDate.delete()
            return JsonResponse({"message":"ok"}, json_dumps_params={'ensure_ascii': False} , status = 200)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

#medicine insert 함수
def med_insert(request, user_uid):
     med = json.loads(request.body) #JSON data parsing
     make_med_uid=uid_num(2)+1#유효아이디 때문에 한것
     medicine = Medicine(
                    med_uid=make_med_uid,
                    user_uid=User.objects.get(pk=user_uid),
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
                    med_company= med["med_company"],
     )
     medicine.save()
     saltSave(med["med_salt"],make_med_uid)
     return "ok"
#med_detail edit 함수
def editMedicine(request, med_uid):
    med_edit = json.loads(request.body) #JSON data parsing
    medicine = Medicine.objects.get(med_uid=med_uid)
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
    #해당 med_uid의 salt를 다 지워버리자
    saltDelete(med_uid)
    #med_salt inset, update함수
    saltSave(med_edit["med_salt"], med_uid)

    return "ok"

#salt detail insert, update 함수
def saltSave(salt_arr, med_uid):
    result = uid_num(1)
    i=1
    for salt in salt_arr:
        if salt["salt_uid"]==0:#salt insert

            med_salt = Med_salt(salt_uid=result+i,
                            med_uid=Medicine.objects.get(pk=med_uid),
                            salt_name=salt["salt_name"],
                            salt_qty=salt["salt_qty"],
                            salt_qty_type=salt["salt_qty_type"],
                            salt_desc=salt["salt_desc"]
                            )
            med_salt.save()
            i=i+1
        else: #salt update (edit)
            print("update if문")
            med_salt = Med_salt(salt_uid=salt["salt_uid"],
                            med_uid=Medicine.objects.get(pk=med_uid),
                            salt_name=salt["salt_name"],
                            salt_qty=salt["salt_qty"],
                            salt_qty_type=salt["salt_qty_type"],
                            salt_desc=salt["salt_desc"]
                            )
            med_salt.save()

def saltDelete(del_uid): #med_salt 삭제 함수
    med_salt = get_object_or_404(Med_salt, med_uid=del_uid) #해당하는 uid salt데이터 가져오고
    med_salt.delete()#  전부 지워버리기

def uid_num(num):
    if num==1:#med_salt uid 증가시키기
        result = Med_salt.objects.all().count()
        return result
    if num==2:#med_uid 증가
        result = Medicine.objects.all().count()
        print(result,"약의 전체 개수 출력")
        return result




