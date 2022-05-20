
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models import Count, OuterRef, Subquery
import json

from .models import Company
from bank.models import Bank
from user.models import User


def checkAuth(request):
    try:
        # sessionid를 통해 사용자 정보를 확인 후 없을경우 404를 띄운다.
        headerAuth = request.session['auth']
        userAuth = get_object_or_404(User, user_uid=headerAuth)
        return userAuth
    except:
        return JsonResponse({'message': 'user not found'}, status=404)


def companyMain(request):
    if request.method == 'GET':  # /company
        userAuth = checkAuth(request)
        page = request.GET['page']
        if int(page) >= 1:
            start = ((int(page) * 10) - 10)
            end = (int(page) * 10)
        else:
            # 잘못된 값이 query로 들어올경우의 예외처리
            return JsonResponse({'message': 'bad input data'}, status=400)
        bankele = list(Bank.objects.all().values())
        companylist = Company.objects.select_related('bank_uid').filter(user_uid=userAuth.user_uid)
        allcount = companylist.count()
        companyele = companylist[start:end]
        bankList = []

        for i in bankele:
            bankList.append({i['bank_uid']: i['bank_name']})
        result = []
        # select_related를 사용하면 아래와 같이 json을 변경해주어야 한다.
        for e in companyele:
            if e.bank_uid == None:
                bankName = ''
            else:
                bankName = e.bank_uid.bank_name
            resultele = {}
            resultele['com_uid'] = e.com_uid
            resultele['com_name'] = e.com_name
            resultele['com_licence_no'] = e.com_licence_no
            resultele['com_address'] = e.com_address
            resultele['com_contact_no'] = e.com_contact_no
            resultele['com_email'] = e.com_email
            resultele['com_description'] = e.com_description
            resultele['com_account_no'] = e.com_account_no
            resultele['bank_name'] = bankName
            resultele['com_joindate'] = e.com_joindate.strftime('%Y-%m-%d')
            result.append(resultele)
        return JsonResponse(
            {'companyallcount': allcount, 'company_list': result, 'bank_list': bankList}
            , json_dumps_params={'ensure_ascii': False}
            , status=200
        )

    elif request.method == 'POST':  # /company
        userAuth = checkAuth(request)

        try:
            inputData = json.loads(request.body.decode('utf-8'))
            check_licence=Company.objects.filter(com_licence_no=inputData['com_licence_no']).count()
            check_address=Company.objects.filter(com_address=inputData['com_address']).count() 
            if check_licence != 0 or check_address !=0 :
                return JsonResponse({'message': 'bad input data'}, safe=False, status=400)
            else:
                try:
                    bank = Bank.objects.get(bank_uid=inputData['bank_uid'])
                    Company.objects.create(
                        com_name=inputData['com_name'],
                        com_licence_no=inputData['com_licence_no'],
                        com_address=inputData['com_address'],
                        com_contact_no=inputData['com_contact_no'],
                        com_email=inputData['com_email'],
                        com_description=inputData['com_description'],
                        com_joindate=inputData['com_joindate'],
                        com_account_no=inputData['com_account_no'],
                        bank_uid=bank,
                        user_uid=userAuth
                    )

                    return JsonResponse(
                        {'message': 'ok'}
                        , safe=False
                        , json_dumps_params={'ensure_ascii': False}
                        , status=200
                    )
                except:
                    return JsonResponse({'message': 'bad input data'}, safe=False, status=400)
        
        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)


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

    if request.method == 'PATCH':  # company/{uid}
        userAuth = checkAuth(request)
        try:
            try:
                targetInfo = Company.objects.get(com_uid=uid, user_uid=userAuth.user_uid)
            except Company.DoesNotExist:
                return JsonResponse({'message': 'unauthorization'}, safe=False, status=401)

            inputdata = json.loads(request.body.decode('utf-8'))
            bank = Bank.objects.get(bank_uid=inputdata['bank_uid'])

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

            return JsonResponse({'message': 'ok'}, status=200)

        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)

    if request.method == 'DELETE':  # company/{uid}
        userAuth = checkAuth(request)
        try:
            try:
                targetInfo = Company.objects.get(com_uid=uid, user_uid=userAuth.user_uid)
            except Company.DoesNotExist:
                return JsonResponse({'message': 'unauthorization'}, safe=False, status=401)

            targetInfo.delete()

            return JsonResponse({'message': 'ok'}, status=200)

        except:
            return JsonResponse({'message': 'bad input data'}, safe=False, status=400)




    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)

