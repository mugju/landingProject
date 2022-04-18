from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator

MAX_LIST_CNT = 10
MAX_PAGE_CNT = 5

import json
from .models import Medicine , Med_salt
from user.models import User

def med_index(request):
    user_uid=141
    if request.method == 'GET':
#         page = request.get('page',1)
        medicine_list = Medicine.objects.filter(user_uid=user_uid)#uer_id session에서 받아오기
#         paginator = Paginator(medicine_list, MAX_LIST_CNT)
#         page_obj = paginator.get_page(page) # paginator.count = 전체 게시물 개수
        company_list = Medicine.objects.filter(user_uid=user_uid).values('med_company') # 제조사 정보만 받아오기
        medicineallcount = Medicine.objects.filter(user_uid=user_uid).count()
        context = {'medicine_list': medicine_list, 'company_list': company_list, 'medicineallcount':medicineallcount}
        return render(request, 'medicine/med_list.html',context)
    else:#POST 방식일때
        message = med_insert(request, user_uid)
        result = {"message" : message}
        return render(request,'medicine/med_list.html')#  medicine add하고 어디로 보내줘야하지? get으로 다시 list 보내주어야하는것인가?





def med_detail(request, med_uid):
    if request.method == 'GET':
        medicine = get_object_or_404(Medicine, pk=med_uid) # med_uid가 uid인 정보 가져오기
        med_salt_list = Med_salt.objects.filter(med_uid=med_uid) #med_uid가 같은 med_salt만 select해오기
        context ={'medicine': medicine, 'med_salt_list': med_salt_list}
        return render(request, 'medicine/med_detail.html',context)

    if request.method == 'PATCH':
        #med_detail update
        edit_med_detail(request, med_uid)
        #salt_detail update, insert, delete
        medicine = get_object_or_404(Medicine, pk=med_uid) # med_uid가 uid인 정보 가져오기
        med_salt_list = Med_salt.objects.filter(med_uid=med_uid) #med_uid가 같은 med_salt만 select해오기
        context ={'medicine': medicine, 'med_salt_list': med_salt_list}
        return render(request, 'medicine/med_detail.html', context)
#medicine insert 함수
def med_insert(request, user_uid):
     med = json.loads(request.body) #JSON data parsing
     make_med_uid=uid_num(2)+1
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
     salt_fun(med["med_salt"],make_med_uid)
     return "ok"
#med_detail edit 함수
def edit_med_detail(request, med_uid):
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
    #med_salt inset, update함수
    salt_fun(med_edit["med_salt"], med_uid)
    #med_salt delete함수
    slat_del(med_edit["med_salt_del"], med_uid)
    return "ok"

#salt detail insert, update 함수
def salt_fun(salt_arr, med_uid):
    result = uid_num(1)
    i=1
    for salt in salt_arr:
        if salt["salt_uid"]==0:#salt 추가 지금 전부다 insert if문으로 들어간다 미쳐버리겠다.

            med_salt = Med_salt(salt_uid=result+i,
                            med_uid=Medicine.objects.get(pk=med_uid),
                            salt_name=salt["salt_name"],
                            salt_qty=salt["salt_qty"],
                            salt_qty_type=salt["salt_qty_type"],
                            salt_desc=salt["salt_desc"]
                            )
            med_salt.save()
            i=i+1
        else: #salt edit
            print("update if문")
            med_salt = Med_salt(salt_uid=salt["salt_uid"],
                            med_uid=Medicine.objects.get(pk=med_uid),
                            salt_name=salt["salt_name"],
                            salt_qty=salt["salt_qty"],
                            salt_qty_type=salt["salt_qty_type"],
                            salt_desc=salt["salt_desc"]
                            )
            med_salt.save()

def slat_del(del_uid, med_uid): #med_salt 삭제 함수
    for del_date in del_uid:
        med_salt = get_object_or_404(Med_salt, pk=del_date)
        med_salt.delete()

def uid_num(num):
    if num==1:#med_salt uid 증가시키기
        result = Med_salt.objects.all().count()
        return result
    if num==2:#med_uid 증가
        result = Medicine.objects.all().count()
        print(result,"약의 전체 개수 출력")
        return result
#     for count, data in enumerate(salt_arr):
#         #salt_uid 여분 판단
#         if[data[0]==0]:# 0일때 유효하이디가 없으면
#             salt_uid_count= salt_uid_count+1 # 임시로 salt_uid 생성
#             new = Msed_salt(
#                 med_uid=med_uid,
#                 salt_uid=salt_uid_count,
#                 salt_name=data[1],
#                 salt_qty=data[2],
#                 salt_qty_type=data[3],
#                 salt_desc=data[4]
#             )
#             creat_salt_list.append(new) #create list 만들기
#         else: # 이미존재하는 salt 일때
#             update = Med_salt(
#                 med_uid=med_uid,
#                 salt_uid=data[0],
#                 salt_name=data[1],
#                 salt_qty=data[2],
#                 salt_qty_type=data[3],
#                 salt_desc=data[4]
#             )
#             update_salt_list.append(update) #update list 만들기
#     if[creat_salt_list != null]:#creat_list에 값이 존재하면
#         Med_salt.objects.bulk_create(creat_salt_list)  # med_salt_list insert하기
#     if[update_salt_list != null]:
#         Med_salt.object.bulk_update(update_salt_list)  # med_salt_list update하기
#     return redirect('<int:med_uid>/')



