from datetime import datetime, timedelta
from django.test import TestCase
from django.test import Client


from .models import Bill
from user.models import User
from config import util
from medicine.models import Medicine

import json


class CompanyTest(TestCase , Bill) :
    def setUp(self) :
        global testuser 
        testuser = User.objects.create_user(
                user_email='test@cnr.com',
                password='123123',
                user_storename='공릉약국'
            )
    
        Bill.objects.create(
            user_uid = testuser,
            bill_total_sell = 0,
            bill_profit = 0,
            bill_date = datetime.now().strftime('%Y-%m-%d')
        )

        Medicine.objects.create(
            user_uid = testuser,
            med_name = 'test약',
            med_type = 'testType',
            med_buyprice = 5000,
            med_sellprice = 7000,
            med_cgst = 50,
            med_sgst = 30,
            med_expire = datetime.now().strftime('%Y-%m-%d'),
            med_mfg = datetime.now().strftime('%Y-%m-%d'),
            med_desc = '먹으면 바로 완치',
            med_instock = 15,
            med_qty = 5,
            med_company = '상봉제약'
        )
          


    getData = [{
        'med_uid':1,
        'med_name':'test약',
        'med_sellprice':7000
    }]
    
    postData = {
       "req_name": "테스트신청2",
        "req_phone": "01028283434",
        "req_med_detail": "post 요청확인",
        "req_joindate":datetime.now().strftime('%Y-%m-%d'),
        "req_status": False,
    }

    patchData = {
        "req_name": "테스트신청3",
        "req_phone": "01028283434",
        "req_med_detail": "patch 요청확인",
        "req_joindate":datetime.now().strftime('%Y-%m-%d'),
        "req_status": False,
    }

    
    def test_company(self, table=Bill, url = '/customer/bill', getdata=getData, postreq = postData, patchreq = patchData): 
        test_uid = Bill.objects.get(user_uid = testuser.user_uid)
        util.instance_get(self, table, url, getdata,'bill get test')
        print('')
        print('')
        util.instacne_post(self, table, '/customer/req', postreq, testuser, 'bill post test')
        print('')
        print('')
        util.instacne_patch(self, table, '/customer/req/{}'.format(test_uid.user_uid), 
        '/customer/bill/{}'.format(3), patchreq, testuser, 'bill patch test' )
        print('')
        print('')
        util.instance_delete(self, '/customer/req/{}'.format(test_uid.user_uid), 
        '/customer/bill/{}'.format(3), 'bill delete test')

