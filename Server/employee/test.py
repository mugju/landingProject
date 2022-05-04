from datetime import datetime, timedelta
from django.test import TestCase

from .models import Employee, Salary
from company.models import Company
from user.models import User
from config import util
from bank.models import Bank

import json


class MedicineTest(TestCase, Employee) :
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

        testEmp = Employee.objects.create(
            user_uid = testuser,
            bank_uid = testbank,
            emp_name = '테스트직원',
            emp_joindate = nowdate.strftime('%Y-%m-%d'),
            emp_phone = '01040492323',
            emp_address = '서울시 강남구',
            emp_account_no = 123123,
            emp_added_on = '2022-03-07'
        )
        Salary.objects.create(
            emp_uid = testEmp,
            sal_date = '2022-05-02',
            sal_amount = 123000,
            sal_joindate = nowdate.strftime('%Y-%m-%d')
        )
        
    data ={
        "employeeallcount": 1,
        "employee_list": [
            {
            "emp_uid": 1,
            "emp_name": "테스트 직원",
            "emp_joindate": datetime.now().strftime('%Y-%m-%d'),
            "emp_phone": "0104-402323",
            "emp_address": "서울시 강남구",
            "emp_added_on": "2022-03-07",
            "emp_account_no": 123123,
            "bank_name": "대구은행",
            "emp_salary": [
                {
                "sal_uid": 1,
                "sal_date": "2022-05-02",
                "sal_amount": 123000,
                "sal_joidate": datetime.now().strftime('%Y-%m-%d')
                }]
            }
        ],
        "bank_list": [{"1": "대구은행"}]
    }

    postdata ={
        "emp_name": "postdata",
        "emp_joindate": "2022-03-21",
        "emp_phone": "01023495293",
        "emp_address": "대구광역시 성당못",
        "emp_account": 1232412412,
        "bank_uid": 1
    }
    

    dummydata = {
        "emp_uid": 1,
        "emp_name": "테스트 직원2",
        "emp_joindate": datetime.now().strftime('%Y-%m-%d'),
        "emp_phone": "0104-402323",
        "emp_address": "서울시 노원구",
        "emp_added_on": "2022-03-07",
        "emp_account_no": 123123,
        "bank_uid": 1,
        "emp_salary": [
            {
            "sal_uid": 1,
            "sal_date": "2022-05-02",
            "sal_amount": 123000,
            "sal_joidate": datetime.now().strftime('%Y-%m-%d')
            }
        ]
    }
    def test_company(self, table=Employee, url = '/employee/?page=1', getdata=data, patchdata = dummydata , postdata = postdata): 
        test_uid = Employee.objects.get(user_uid = testuser.user_uid)
        util.instance_get(self, table, url, getdata,'employee get test')
        print('')
        print('')
        util.instacne_post(self, table, '/employee/', postdata, testuser, 'employee post test')
        print('')
        print('')
        util.instacne_patch(self, table, '/employee/{}'.format(test_uid.emp_uid), 
        '/company/{}'.format(2), patchdata, testuser, 'employee patch test' )
        print('')
        print('')
        util.instance_delete(self,  '/employee/{}'.format(test_uid.emp_uid), 
        '/company/{}'.format(2), 'employee delete test')

