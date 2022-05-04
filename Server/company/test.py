from datetime import datetime, timedelta
from django.test import TestCase
from django.test import Client

from bank.models import Bank
from .models import Company
from user.models import User
from config import util

import json


class CompanyTest(TestCase , Company) :
    def setUp(self) :
        global testuser 
        testuser = User.objects.create_user(
                user_email='test@cnr.com',
                password='123123',
                user_storename='공릉약국'
            )
        testbank = Bank.objects.create(bank_name = '대구은행')
        global nowdate 
        nowdate = datetime.now()
        global dummydata
        Company.objects.create(
            com_name = '씨엔알리서치',
            com_licence_no = '1234',
            com_address = '서울시 노원구',
            com_contact_no = '01049403499',
            com_email = 'baek1008@cnrrr.com',
            com_description = '그만해~~',
            com_joindate = nowdate.strftime('%Y-%m-%d'),
            com_account_no = '166131495032',
            user_uid = testuser,
            bank_uid = testbank
        )
    data ={
        'companyallcount': 1, 
        'company_list': [
            {
            'com_uid': 1, 
            'com_name': '씨엔알리서치', 
            'com_licence_no': '1234', 
            'com_address': '서울시 노원구', 
            'com_contact_no': '01049403499', 
            'com_email': 'baek1008@cnrrr.com', 
            'com_description': '그만해~~', 
            'com_account_no': '166131495032', 
            'bank_name': '대구은행', 
            'com_joindate': datetime.now().strftime('%Y-%m-%d')
            }
            ], 
            'bank_list': [{'1':'대구은행'}]
            }

    dummydata = {
        "com_uid": 1,
        "com_name": "원자력",
        "com_licence_no": "asdas123",
        "com_address": "대구광역시 중구",
        "com_contact_no": '1012312123',
        "com_email": "baek1008@asd.com",
        "com_description": "이편지는 영구에서",
        "com_joindate": datetime.now().strftime('%Y-%m-%d'),
        "com_account_no":' 1234512354',
        "bank_uid": 1
    }
    def test_company(self, table=Company, url = '/company/?page=1', testdata=data, patchdata = dummydata): 
        test_uid = Company.objects.get(user_uid = testuser.user_uid)
        util.instance_get(self, table, url, testdata,'company get test')
        print('')
        print('')
        util.instacne_post(self, table, '/company/', patchdata, testuser, 'company post test')
        print('')
        print('')
        util.instacne_patch(self, table, '/company/{}'.format(test_uid.com_uid), 
        '/company/{}'.format(3), patchdata, testuser, 'company patch test' )
        print('')
        print('')
        util.instance_delete(self, '/company/{}'.format(test_uid.com_uid), 
        '/company/{}'.format(3), 'company delete test')

