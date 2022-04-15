from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse
from django.db.models import Count , OuterRef , Subquery
import json


from .models import Company
from bank.models import Bank
from user.models import User

def checkAuth(headers):
    try:
        headerAuth = headers['auth']
        userAuth = get_object_or_404( User, user_session = headerAuth)
    except User.DoesNotExist:
        return JsonResponse({'message': 'unauthorized users'})
    finally:
        return userAuth 


def companyMain(request):
    if request.method == 'GET': #/company 
        try:
            headerAuth = request.headers['auth']
            userAuth = get_object_or_404( User, user_session = headerAuth)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

        try:
            # userAuth = checkAuth(request.headers)
            page = request.GET['page']
            if page != 1:
                start = ((int(page) * 10) - 10)
                end = (int(page) * 10)
    
            allcount = Company.objects.filter(user_uid = userAuth.user_uid).count()
            bankele = list(Bank.objects.all().values())
            companyele = list(Company.objects.select_related('bank_uid').filter(user_uid = userAuth.user_uid))[start:end]
                    # .annotate(companyallcount = Subquery(Company.objects.filter(com_uid = OuterRef('pk'))\
                    # .values('com_uid').annotate(count = Count('pk')).values('count'))))
            bankList = []
            for i in bankele:
                    bankList.append({i['bank_uid'] : i['bank_name']})
            result = []
            for e in companyele:
                    resultele = {}
                    resultele['com_uid'] = e.com_uid
                    resultele['com_name'] = e.com_name
                    resultele['com_licence_no'] = e.com_licence_no
                    resultele['com_address'] = e.com_address
                    resultele['com_contact_no'] = e.com_contact_no
                    resultele['com_email'] = e.com_email
                    resultele['com_description'] = e.com_description
                    resultele['com_account_no'] = e.com_account_no
                    resultele['bank_name'] = e.bank_uid.bank_name
                    target = e.com_joindate.strftime('%Y-%m-%d')
                    resultele['com_joindate'] = target
                    result.append(resultele)

            return JsonResponse(
                    {'companyallcount' : allcount,'company_list': result , 'bank_list': bankList}
                    , json_dumps_params={'ensure_ascii': False} 
                    , status = 200 
                    )
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))
       
    if request.method == 'POST': #/company
        try:
            headerAuth = request.headers['auth']
            userInfo = get_object_or_404( User , user_session = headerAuth)
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))

        try:
            inputdata = json.loads(request.body.decode('utf-8'))
            bank = Bank.objects.get(bank_uid = inputdata['bank_uid'])

            Company.objects.create(
                com_name = inputdata['com_name'],
                com_licence_no = inputdata['com_licence_no'],
                com_address = inputdata['com_address'],
                com_contact_no = inputdata['com_contact_no'],
                com_email = inputdata['com_email'],
                com_description = inputdata['com_description'],
                com_joindate = inputdata['com_joindate'],
                com_account_no = inputdata['com_account_no'],
                bank_uid = bank,
                user_uid = userInfo
            )
            return JsonResponse(
                    inputdata
                    , safe= False
                    , json_dumps_params={'ensure_ascii': False} 
                    , status = 200 
                    )
        except:
            return HttpResponseBadRequest(json.dumps('Bad request'))
        
def companyDetail(request, uid):            
    # if request.method == 'GET': #company/{uid}

    #     try:
    #         headerAuth = request.headers['auth']
    #         userAuth = get_object_or_404( User ,user_session = headerAuth)
    #         targetInfo = Company.objects.select_related('bank_uid').get(com_uid = uid) 

    #         result = {}
    #         result['com_uid'] = targetInfo.com_uid
    #         result['com_name'] =targetInfo.com_name
    #         result['com_licence_no'] = targetInfo.com_licence_no
    #         result['com_address'] = targetInfo.com_address
    #         result['com_contact_no'] = targetInfo.com_contact_no
    #         result['com_email'] = targetInfo.com_email
    #         result['com_description'] = targetInfo.com_description
    #         result['com_joindate'] = targetInfo.com_joindate.strftime('%Y-%m-%d')
    #         result['com_account_no'] = targetInfo.com_account_no
    #         result['bank_name'] = targetInfo.bank_uid.bank_name

    #         return JsonResponse(
    #                 result
    #                 , safe= False
    #                 , json_dumps_params={'ensure_ascii': False} 
    #                 , status = 200 
    #                 )
    #     except:
    #         return HttpResponseBadRequest(json.dumps('Bad request'))

    if request.method == 'PATCH': #company/{uid}

        try:
            headerAuth = request.headers['auth']
            userAuth = get_object_or_404( User ,user_session = headerAuth)
        except:
            return HttpResponse(('Bad request'), status = 400)

        try:
            targetInfo = Company.objects.get(com_uid = uid, user_uid = userAuth.user_uid) 
            inputdata = json.loads(request.body.decode('utf-8'))
            bank = Bank.objects.get(bank_uid = inputdata['bank_uid'])

            targetInfo.com_name = inputdata['com_name']
            targetInfo.com_licence_no = inputdata['com_licence_no']
            targetInfo.com_address = inputdata['com_address']
            targetInfo.com_contact_no = inputdata['com_contact_no']
            targetInfo.com_email = inputdata['com_email']
            targetInfo.com_description = inputdata['com_description']
            targetInfo.com_joindate = inputdata['com_joindate']
            targetInfo.com_account_no = inputdata['com_account_no']
            targetInfo.bank_uid = bank
            targetInfo.save()
            return JsonResponse({'message': 'Ok'}, status = 200)
        except Company.DoesNotExist:
            return HttpResponse(('Bad request'), status = 400)
        except:    
            return HttpResponse(('Bad request'), status = 400)

    elif request.method == 'DELETE': #company/{uid}
        try:
            headerAuth = request.headers['auth']
            userAuth = get_object_or_404( User ,user_session = headerAuth)
        except:
            return HttpResponse(('Bad request'), status = 400)
        
        try:
            targetInfo = Company.objects.get(com_uid = uid, user_uid = 5) #userAuth.uid가 들어가야함    
            targetInfo.delete()
            return JsonResponse({'message': 'Ok'}, status = 200)

        except Company.DoesNotExist:
            return HttpResponse(('Bad request'), status = 400)
        except:    
            return HttpResponse(('Bad request'), status = 400)
        
    else:
        return HttpResponse(('Bad request'), status = 400)

