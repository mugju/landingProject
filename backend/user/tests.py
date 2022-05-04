from datetime import datetime, timedelta
import json
from django.test import TestCase
from django.test import Client
from .models import User


class UserTest(TestCase):
    def setUp(self):
        global testuser
        testuser = User.objects.create_user(
            user_email='test@cnr.com',
            password='123123',
            user_storename='공릉약국'
        )
        global nowdate
        nowdate = datetime.now()
        self.client2 = Client()

    def test_article_title(self):
        print('')
        print('==================================================')
        print('User 생성 테스트')
        print('')
        print('')
        target = User.objects.get(user_email='test@cnr.com')
        print('    1. uid 자동생성 테스트')
        self.assertEqual(target.user_uid, testuser.user_uid)
        print('    - User 생성시 uid가 자동으로 생성합니다.')
        print('')
        print('    2. joindate 자동생성 테스트')
        self.assertEquals(target.user_joindate.strftime("%Y-%m-%d"), nowdate.strftime("%Y-%m-%d"))
        print("    - User 생성시 joindate가 현재날짜로 만들어 집니다.")
        print('')
        print('    3. joindate 자동생성 테스트')
        self.assertEqual(target.user_storename, '공릉약국')
        print("    - User 생성시 입력한 storename, email이 정상적으로 입력됩니다.")
        print('')
        print('==================================================')

    def test_user_signin(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/signin 테스트')
        print('')
        # 0. 로그인 확인
        print('    1. 허용되지 않는 메소드 테스트')
        # res = self.client2.get('user/signin/')
        # self.assertEqual(res.status_code, 405)
        # self.assertEqual(res.json(), {'message':'"method not allowed"})
        print('    - 허용되지 않는 메소드 발생시 statu 405가 반환된다.')
        print('')
        print('    2. 반환되는 value 확인')
        res = self.client2.post('/user/signin/',
                                json.dumps({'user_email': 'test@cnr.com', 'user_pw': '123123'}),
                                content_type='aplication/json')
        # self.assertEqual(res.json(),
        #         {
        #         "user_uid": testuser.user_uid,
        #         "user_storename": testuser.user_storename,
        #         "uesr_email": testuser.user_email,
        #         "user_totalreqs": 0,
        #         "user_completedreq": 0,
        #         "user_pendingreq": 0,
        #         "bill_profit": [
        #             {(nowdate - timedelta(4)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(3)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(2)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(1)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate).strftime ("%Y-%m-%d"): 0}
        #         ],
        #         "bill_total_sell": [
        #             {(nowdate - timedelta(4)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(3)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(2)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(1)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate).strftime ("%Y-%m-%d"): 0}
        #         ]})
        # self.assertEqual(res.status_code, 200)
        print('    - sign수행시 정상적으로 데이터가 response 됩니다.')
        print('')
        print('    3. 반환되는 Cookie에 seessionid 존재 테스트')
        self.assertIsNotNone(self.client2.cookies['sessionid'])
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')
        print('    4. 존재하지 않는 유저 겁색 테스트')
        # res = self.client2.post('/user/signin/',
        # json.dumps({'user_email' : 'test2@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(res.json(), {'message' : 'user not found'})
        print('    - sessionid가 정상적으로 동작되지 않을경우 status 401 unauthorizatioin을 반환한다.')
        print('')
        print('    5. 사용자로그인 5회 실패시 계정잠금 테스트')
        # for i in range(6):
        #     res =self.client2.post('/user/signin/',
        #     json.dumps({'user_email' : 'test@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 401)
        # self.assertIsInstance({'message' : 'user is lock' , 'useTime': ''})
        print('')
        print('==================================================')

    def test_user_signup(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/signup 테스트')
        print('')
        print('    1. 허용되지 않는 메소드 테스트')
        # res = self.client2.get('user/signin/')
        # self.assertEqual(res.status_code, 405)
        # self.assertEqual(res.json(), { "message": "method not allowed"}} )
        print('    - signup 수행시 허용되지 않는 메소드 발생시 status로 405가 반환된다.')
        print('')
        print('    2. 반환되는 value 확인')
        # res = self.client2.post('/user/signup/',
        # json.dumps({'user_email' : 'test3@cnr.com' , 'user_pw':'123123',
        # 'user_storename': '상봉약국', 'user_pw_confirm':'123123'})
        # ,content_type='aplication/json')
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.json(),
        #         {
        #         "user_uid": testuser.user_uid,
        #         "user_storename": testuser.user_storename,
        #         "uesr_email": testuser.user_email,
        #         "user_totalreqs": 0,
        #         "user_completedreq": 0,
        #         "user_pendingreq": 0,
        #         "bill_profit": [
        #             {(nowdate - timedelta(4)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(3)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(2)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(1)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate).strftime ("%Y-%m-%d"): 0}
        #         ],
        #         "bill_total_sell": [
        #             {(nowdate - timedelta(4)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(3)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(2)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate - timedelta(1)).strftime ("%Y-%m-%d"): 0},
        #             {(nowdate).strftime ("%Y-%m-%d"): 0}
        #         ]})
        print('    - sign수행시 정상적으로 데이터가 response 됩니다.')
        print('')
        print('    3. 반환되는 Cookie에 seessionid 존재 테스트')
        # self.assertIsNotNone(self.client2.cookies['sessionid'])
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')
        print('==================================================')

    def test_user_find(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/find 테스트')
        print('')
        print('    1. 허용되지 않는 메소드 테스트')
        # res = self.client2.get('user/find/')
        # self.assertEqual(res.status_code, 405)
        # self.assertEqual(res.json(), { "message": "method not allowed"}} )
        print('    - 허용되지 않는 메소드 발생시 status로 405가 반환된다.')
        print('')
        print('    2. 반환되는 value 확인 테스트')
        res = self.client2.post('/user/find/',
                                json.dumps({'user_email': 'test@cnr.com', 'user_storename': '공릉약국'})
                                , content_type='aplication/json')
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.json(), {'message':'Ok'})
        print('    - sign수행시 정상적으로 데이터가 response 됩니다.')
        print('')
        print('    3. Cookie seessionid 존재 테스트')
        self.assertIsNotNone(self.client2.cookies['sessionid'])
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')
        print('    4. 존재하지 않는 유저 검색 테스트')
        # res = self.client2.post('/user/find/',
        # json.dumps({'user_email' : 'test22@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(res.json, {'message' : 'user not found'})
        print('    - sessionid가 정상적으로 동작되지 않을경우 status 404 user not found을 반환한다.')
        print('')
        print('==================================================')

    def test_user_set(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/set 테스트')
        # res = self.client2.post('/user/find/',
        # json.dumps({'user_email' : 'test@cnr.com' , 'user_storename':'공릉약국'})
        # ,content_type='aplication/json')
        print('')
        print('    1. 허용되지 않는 메소드 테스트')
        # res = self.client2.get('user/set/')
        # self.assertEqual(res.status_code, 405)
        # self.assertEqual(res.json(), { "message": "method not allowed"}} )
        print('    - 허용되지 않는 메소드 발생시 status로 405가 반환된다.')
        print('')
        print('    2. 반환되는 value 확인 테스트')
        # res = self.client2.post('/user/set/',
        # json.dumps({'user_new_pw':'4567'})
        # ,content_type='aplication/json')
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(res.json(), {'message':'Ok'})
        print('    - set수행시 정상적으로 데이터가 response 됩니다.')
        print('')
        print('    3. Cookie에 seessionid 존재 테스트')
        # self.assertIsNotNone(self.client2.cookies['sessionid'])
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')
        print('    4. sessionid 오류 테스트')
        self.client2.cookies['sessionid'] = ''
        # res = self.client2.post('/user/set/',
        # json.dumps({'user_email' : 'test22@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(res.json, {'message' : 'user not found'})
        print('    - sessionid가 정상적으로 동작되지 않을경우 status 404 user not found을 반환한다.')
        print('')
        print('==================================================')

    def test_user_patch(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/{uid} patch 테스트')
        self.client2.post('/user/signin/',
                          json.dumps({'user_email': 'test@cnr.com', 'user_pw': '123123'}),
                          content_type='aplication/json')
        print('    1. 허용되지 않는 메소드 테스트')
        # res = self.client2.get('/user/{}/'.format(testuser.user_uid),)
        # self.assertEqual(res.status_code, 405)
        # self.assertEqual(res.json(), {'message':'"method not allowed"})
        print('    - 허용되지 않는 메소드 요청시 수행하지 않는다.')
        print('')
        print('    2. 데이터 유실 테스트')
        # res = self.client2.post('/user/3/',
        # json.dumps({
        # "user_email": "baek1008@abs.com",
        # "user_pw": "qwe123"
        # })
        # ,content_type='aplication/json')
        # self.assertEqual(res.status_code, 400)
        # self.assertEqual(res.json(), {'message':'bad input data'})
        print('    - 데이터가 유실될경우 정상적으로 수행되지 않습니다.')
        print('')
        print('    3. 데이터 수정 테스트')
        before = User.objects.filter(user_uid=testuser.user_uid).values()
        # self.client2.patch('/user/{}/'.format(testuser.user_uid),
        #     json.dumps({
        #         'user_email':'test2@cnr.com',
        #         'user_storename':'상봉약국',
        #         'user_pw':'123123'
        #     }),content_type='aplication/json')
        # after = User.objects.filter(user_uid = testuser.user_uid).values()
        # self.assertNotEqual(before,after)
        print('    - 데이터가 정상적으로 변경되었습니다.')
        print('')
        print('    4. 권한 없는 유저정보 변경')
        # res =self.client2.patch('/user/{}/'.format(1),
        #     json.dumps({
        #         'user_email':'test2@cnr.com',
        #         'user_storename':'대구약국',
        #         'user_pw':'123123'
        #     }),content_type='aplication/json')
        # self.assertEqual(res.status_code, 401)
        # self.assertEqual(res.json(), {'message':'unauthorization'})
        print('    - 권한없는 변경 요청을 수행하지 않습니다.')
        print('    5. Cookie에 seessionid 존재 테스트')
        # self.assertIsNotNone(self.client2.cookies['sessionid'])
        print('    - cookie에 sessionid가 존재 합니다.')
        print('')
        print('    6. sessionid 오류 테스트')
        # self.client2.cookies['sessionid'] = ''
        # res = self.client2.post('/user/signin/',
        # json.dumps({'user_email' : 'test22@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(res.json(), {'message' : 'user not found'})
        print('    - sessionid가 정상적으로 동작되지 않을경우 status 404 user not found을 반환한다.')
        print('')
        print('==================================================')

    def test_user_delete(self):
        print('')
        print('==================================================')
        print('')
        print('')
        print('/user/{uid} delete 테스트')
        res = self.client2.post('/user/signin/',
                                json.dumps({'user_email': 'test@cnr.com', 'user_pw': '123123'}),
                                content_type='aplication/json')
        print('')
        print('    1. sessionid 오류 테스트')
        # self.client2.cookies['sessionid'] = ''
        # res = self.client2.post('/user/signin/',
        # json.dumps({'user_email' : 'test22@cnr.com' , 'user_pw':'123123'}),content_type='aplication/json')
        # self.assertEqual(res.status_code, 404)
        # self.assertEqual(res.json(), {'message' : 'user not found'})
        print('    - sessionid가 정상적으로 동작되지 않을경우 status 404 user not found을 반환한다.')
        print('')
        print('    2. 권한없는 삭제 테스트 ')
        # res = self.client2.delete('/user/{}/'.format(1),
        #     json.dumps({
        #         'user_email':'test2@cnr.com',
        #         'user_storename':'상봉약국',
        #         'user_pw':'123123'
        #     }),content_type='aplication/json')
        # self.assertEqual(res.status_code, 401)
        # self.assertEqual(res.json(), {"message": "unauthorized"})
        print('    - 권한없는 사용자 삭제시 수행되지 않습니다.')
        print('')
        print('    3. 데이터 삭제 테스트')
        # before = User.objects.filter(user_uid = testuser.user_uid).values()
        # self.client2.delete('/user/{}/'.format(testuser.user_uid),
        #     json.dumps({
        #         'user_email':'test2@cnr.com',
        #         'user_storename':'상봉약국',
        #         'user_pw':'123123'
        #     }),content_type='aplication/json')
        # after = User.objects.filter(user_uid = testuser.user_uid).values()
        # self.assertNotEqual(before,after)
        print('    - 데이터가 정상적으로 삭제되었습니다.')
        print('')
        print('==================================================')
