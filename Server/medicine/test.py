from datetime import datetime, timedelta
from django.test import TestCase

from .models import Med_salt, Medicine
from company.models import Company
from user.models import User
from config import util
from bank.models import Bank

import json


class MedicineTest(TestCase, Medicine) :
    def setUp(self) :
        global testuser 
        global nowdate 
        global dummydata
        
        nowdate = datetime.now()

        testuser = User.objects.create_user(
                user_email='test@cnr.com',
                password='123123',
                user_storename='공릉약국'
        )
        testbank = Bank.objects.create(bank_name = '대구은행')

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

        testMed = Medicine.objects.create(
            user_uid = testuser,
            med_name = 'test약',
            med_type = 'testType',
            med_buyprice = 5000,
            med_sellprice = 7000,
            med_cgst = 50,
            med_sgst = 30,
            med_expire = nowdate.strftime('%Y-%m-%d'),
            med_mfg = nowdate.strftime('%Y-%m-%d'),
            med_desc = '먹으면 바로 완치',
            med_instock = 15,
            med_qty = 5,
            med_company = '상봉제약'
        )
      
        Med_salt.objects.create(
            salt_name = '염라',
            salt_qty = 10,
            salt_qty_type = 'Tablet',
            salt_desc = '만병통치약',
            med_uid = testMed
        )
        
    data ={
        "medicineallcount": 1,
        "medicine_list": [
            {
            "med_uid": 1,
            "med_name": "test약",
            "med_type": "testType",
            "med_buyprice": 5000,
            "med_sellprice": 7000,
            "med_cgst": 50,
            "med_sgst": 30,
            "med_expire": datetime.now().strftime('%Y-%m-%d'),
            "med_mfg": datetime.now().strftime('%Y-%m-%d'),
            "med_desc": "먹으면 바로 완치",
            "med_instock": 15,
            "med_qty": 5,
            "med_company": "상봉제약",
            "med_salt": [
                {
                "salt_uid": 1,
                "salt_name": "염라",
                "salt_qty": 10,
                "salt_qty_tyep": "Tablet",
                "salt_desc": "만병통치약"
                }
            ]
            }
        ],
        "company_list": [{"1": "씨엔알리서치"}]
    }

    dummydata = {
        "med_uid": 1,
        "med_name": "게보린",
        "med_type": "tablet",
        "med_buyprice": 2500,
        "med_sellprice": 4500,
        "med_cgst": 15,
        "med_sgst": 20,
        "med_expire": "2022-01-12",
        "med_mfg": "2020-04-22",
        "med_desc": "두통,치통,생리통",
        "med_instock": 250,
        "med_qty": 5,
        "med_company": "OO제약",
        "med_salt": [
            {
            "salt_uid": 1,
            "salt_name": "약1",
            "salt_qty": 10,
            "salt_qty_tyep": "tablet",
            "salt_desc": "항생제"
            }
        ]
    }
    def test_company(self, table=Medicine, url = '/medicine/?page=1', getdata=data, postpatchdata = dummydata): 
        test_uid = Medicine.objects.get(user_uid = testuser.user_uid)
        util.instance_get(self, table, url, getdata,'medicine get test')
        print('')
        print('')
        util.instacne_post(self, table, '/medicine/', postpatchdata, testuser, 'medicine post test')
        print('')
        print('')
        util.instacne_patch(self, table, '/medicine/{}'.format(test_uid.med_uid), 
        '/company/{}'.format(2), postpatchdata, testuser, 'medicine patch test' )
        print('')
        print('')
        util.instance_delete(self, '/medicine/{}'.format(test_uid.med_uid), 
        '/company/{}'.format(2),'medicine delete test')

