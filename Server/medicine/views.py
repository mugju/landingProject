from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Medicine , Med_salt
# from django.views.decorators.csrf import csrf_exempt #POST 방식으로 할때 403 에러 때문 (CSRF 검증에 실패했습니다. 요청을 중단하였습니다.)
# @csrf_exempt
# def search(request):
#     return HttpResponse('success')
# Create your views here.

def med_index(request):
    user_uid=141
    if request.method == 'GET':
        medicine_list = Medicine.objects.filter(user_uid=user_uid)#uer_id session에서 받아오기
        company_list = Medicine.objects.filter(user_uid=user_uid).values('med_company') # 제조사 정보만 받아오기
        context = {'medicine_list': medicine_list, 'company_list': company_list}
        return render(request, 'medicine/med_list.html',context)
    else:#POST 방식일때
        medicine_list = Medicine.objects.filter(user_uid=user_uid)#uer_id session에서 받아오기
        context = {'medicine_list': medicine_list}
        return render(request, 'medicine/med_list.html',context)
        #commit test




def med_detail(request, med_uid):
    medicine = get_object_or_404(Medicine, pk=med_uid) # med_uid가 uid인 정보 가져오기
    med_salt_list = Med_salt.objects.filter(med_uid=med_uid) #med_uid가 같은 med_salt만 select해오기
    context ={'medicine': medicine, 'med_salt_list': med_salt_list}
    return render(request, 'medicine/med_detail.html',context)

# salt_add 소금 추가
creat_salt_list=[]
update_salt_list=[]
salt_uid_count=Med_salt.objects.last().salt_uid #제일 마지막 salt_uid 가져오기
#         [0, "saltname테스트", 1, 'T',"약설명 테스트"],salt_uid, salt_name, salt_qty,salt_qty_type, salt_desc
def salt_add(request,med_uid):
    for count, data in enumerate(request.saltlist):
        #salt_uid 여분 판단
        if[data[0]==0]:# 0일때 유효하이디가 없으면
            salt_uid_count= salt_uid_count+1 # 임시로 salt_uid 생성
            new = Med_salt(
                med_uid=med_uid,
                salt_uid=salt_uid_count,
                salt_name=data[1],
                salt_qty=data[2],
                salt_qty_type=data[3],
                salt_desc=data[4]
            )
            creat_salt_list.append(new) #create list 만들기
        else: # 이미존재하는 salt 일때
            update = Med_salt(
                med_uid=med_uid,
                salt_uid=data[0],
                salt_name=data[1],
                salt_qty=data[2],
                salt_qty_type=data[3],
                salt_desc=data[4]
            )
            update_salt_list.append(update) #update list 만들기
    if[creat_salt_list != null]:#creat_list에 값이 존재하면
        Med_salt.objects.bulk_create(creat_salt_list)  # med_salt_list insert하기
    if[update_salt_list != null]:
        Med_salt.object.bulk_update(update_salt_list)  # med_salt_list update하기
    return redirect('<int:med_uid>/')



#=============리스트 방식============
#         if[Med_salt.objects.get(salt_uid=salt_uid[count])==null]: # salt_uid가 없으면
#             # salt_uid 생성 해야한다.
#             salt_uid_count= salt_uid_count+1
#             new = Med_salt(med_uid=med_uid, salt_uid=salt_uid_count, salt_name=salt_name[count],salt_qty=salt_qty[count],
#                            salt_qty_type=salt_qty_type[count], salt_desc=salt_desc[count])
#             creat_list.append(new) #med_salt_list 만들기
#         else:
#             update = Med_salt(salt_name=salt_name[count],salt_qty=salt_qty[count],
#                               salt_qty_type=salt_qty_type[count], salt_desc=salt_desc[count])
#             update_salt_list.append(update)# update list 만들기

# def salt_create(request, med_uid):


