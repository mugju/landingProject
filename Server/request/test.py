from datetime import datetime, timedelta
from django.test import TestCase
from django.test import Client


from .models import Cus_req
from user.models import User
from config import util

import json


class CompanyTest(TestCase , Cus_req) :
    def setUp(self) :
        global testuser 
        testuser = User.objects.create_user(
                user_email='test@cnr.com',
                password='123123',
                user_storename='공릉약국'
            )
    
        Cus_req.objects.create(
            user_uid = testuser,
            req_name = '테스트신청1',
            req_phone = '01049403499' ,
            req_med_detail = '테스트 request',
            req_joindate = datetime.now().strftime('%Y-%m-%d'),
            req_status = False
        )
        
    def instacne_request_patch(self, table, url, testurl , inputdata, testuser,title):
        self.client = Client()
        print('==================================================')
        print(title)
        print(url)
        print('')
        print('')
        # cookie에 sessionid를 set한다.
        res = self.client.post('/user/signin/', 
        json.dumps({'user_email':'test@cnr.com', 'user_pw':'123123'}),
        content_type='aplication/json')

        print('    0. Cookie에 seessionid 존재 테스트')
        self.assertIsNotNone(self.client.cookies['sessionid']) 
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')

        print('    1. 허용되지 않는 메소드 테스트')
        res = self.client.get(url,{})
        self.assertEqual(res.status_code, 405) 
        self.assertEqual(res.json(), {'message':"method not allowed"})
        print('    - 허용되지 않는 메소드 발생시 statu 405가 반환된다.')
        print('')

        print('    2. 권한 없는 데이터변경 테스트')
        res =self.client.patch(testurl,
        json.dumps(inputdata),content_type='aplication/json')
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {'message':'unauthorization'})
        print('    - 권한없는 변경 요청은 status401과 unauthorization 반환합니다.')
        print('')

        print('    3. 데이터 변경 테스트')
        print(url)
        before = table.objects.filter(user_uid = testuser.user_uid).values()
        res = self.client.patch(url,json.dumps(inputdata),content_type='aplication/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'message':'ok'})
        after = table.objects.filter(user_uid = testuser.user_uid).values()
        self.assertNotEqual(before,after)
        print('    - 변경 성공시 status200과 ok를 반환합니다.')

        print('')
        print('==================================================')

    data = [{
        "req_uid" : 1,
        "req_name": "테스트신청1",
        "req_phone": "01049403499",
        "req_med_detail": "테스트 request",
        "req_joindate": datetime.now().strftime('%Y-%m-%d'),
        "req_status": False,
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

    
    def test_company(self, table=Cus_req, url = '/customer/req', testdata=data, postreq = postData, patchreq = patchData
    ,req = instacne_request_patch): 
        test_uid = Cus_req.objects.get(user_uid = testuser.user_uid)
        util.instance_get(self, table, url, testdata,'request get test')
        print('')
        print('')
        util.instacne_post(self, table, '/customer/req', postreq, testuser, 'request post test')
        print('')
        print('')
        req(self, table, '/customer/req/{}'.format(test_uid.user_uid.user_uid), 
        '/customer/req/{}'.format(5), patchreq, testuser, 'request patch test' )
        print('')
        print('')
        util.instance_delete(self, '/customer/req/{}'.format(test_uid.user_uid.user_uid), 
        '/customer/req/{}'.format(5), 'request delete test')

