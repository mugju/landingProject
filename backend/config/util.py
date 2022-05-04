from datetime import datetime, timedelta
from select import select
from traceback import print_tb
from django.test import Client
import json

#table : 작성될 테이블
#url : 사용할 url
#testurl : dummyurl(권한없는 uid 입력)
#inputdata : 들어갈 데이터
#testuser : 테스트간 사용될 가짜 사용자

def instance_get(self, table , url, data,title):
    self.client = Client()
    print('==================================================')
    print(title)
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
    res = self.client.put(url)
    self.assertEqual(res.status_code, 405)
    self.assertEqual(res.json(), {'message':"method not allowed"})
    print('    - 허용되지 않는 메소드 발생시 statu 405가 반환된다.')
    print('')

    print('    2. 반환값 확인 테스트')
    res = self.client.get(url)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.json(), data)
    print('    - 정상적으로 status 200 과 값을 반환합니다.')

    print('')
    print('==================================================')


def instacne_post(self, table, url, data, testuser,title):
    self.client = Client()
    print('==================================================')
    print(title)
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
    res = self.client.put(url)
    self.assertEqual(res.status_code, 405)
    self.assertEqual(res.json(), {'message':"method not allowed"})
    print('    - 허용되지 않는 메소드 발생시 statu 405가 반환된다.')
    print('')

    print('    2. 유실데이터 작성 테스트')
    res = self.client.post(url,json.dumps({"user_uid" : 2}),content_type='aplication/json')
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.json(), {'message':'bad input data'})
    print('    - 데이터가 유실될경우 status400 과 bad inpu data가 반환됩니다.')
    print('')

    print('    3. 데이터 작성 테스트')
    before = table.objects.filter(user_uid = testuser.user_uid)
    res = self.client.post(url,json.dumps(data),content_type='aplication/json')
    after = table.objects.filter(user_uid = testuser.user_uid)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.json(), {'message':'ok'})
    self.assertNotEqual(before,after)
    print('    - 데이터가 정상적으로 작성 되어 status 200과 ok를 반환합니다.')
    print('')
    print('==================================================')


def instacne_patch(self, table, url, testurl , inputdata, testuser,title):
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

    print('    2. 유실데이터 작성 테스트')
    res = self.client.patch(url,json.dumps({"user_uid" : 2}),content_type='aplication/json')
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.json(), {'message':'bad input data'})
    print('    - 데이터가 유실될경우 status400 과 bad inpu data가 반환됩니다.')
    print('')

    print('    3. 권한 없는 데이터변경 테스트')
    res =self.client.patch(testurl,
    json.dumps(inputdata),content_type='aplication/json')
    self.assertEqual(res.status_code, 401)
    self.assertEqual(res.json(), {'message':'unauthorization'})
    print('    - 권한없는 변경 요청은 status401과 unauthorization 반환합니다.')
    print('')

    print('    4. 데이터 변경 테스트')
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

def instance_delete(self, url, testurl, title):
    self.client = Client()
    print('==================================================')
    print(title)
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
    res = self.client.put(url,'')
    self.assertEqual(res.status_code, 405)
    self.assertEqual(res.json(), {'message':"method not allowed"})
    print('    - 허용되지 않는 메소드 발생시 statu 405가 반환된다.')
    print('')

    print('    2 권한 없는 데이터삭제 테스트')
    res =self.client.delete(testurl,content_type='aplication/json')
    self.assertEqual(res.status_code, 401)
    self.assertEqual(res.json(), {'message':'unauthorization'})
    print('    - 권한없는 변경 요청은 status401과 unauthorization 반환합니다.')
    print('')

    # print('    4. 데이터 삭제 테스트')
    # before = table.objects.filter(user_uid = testuser.user_uid).values()
    # res = self.client.delete(url,content_type='aplication/json')
    # self.assertEqual(res.status_code, 200)
    # self.assertEqual(res.json(), {'message':'ok'})
    # after = table.objects.filter(user_uid = testuser.user_uid).values()
    # self.assertNotEqual(before,after)
    # print('    - 삭제 성공시 status200과 ok를 반환합니다.')
    # print('')
    # print('==================================================')