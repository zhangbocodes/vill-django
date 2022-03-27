import json
import logging
import time
import re
import sys
import os
from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from wxcloudrun.models import User
from wxcloudrun.models import History
from wxcloudrun.models import Country
import pandas as pd   # 导入pandas 并重命名 pd
import io
from aip import AipOcr
import requests
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger('log')


def getuser(request):
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    try:
        data = User.objects.get(name="liuwenrui")
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.name},
                        json_dumps_params={'ensure_ascii': False})

def insertUser(request):
    firt = request.POST['first']
    name = request.POST['name']
    password = request.POST['password']
    object1 = User(name = name,password = password, role = 1, countryid = firt)
    rsp = JsonResponse({'code': 0, 'errorMsg': '增加成功'},
                       json_dumps_params={'ensure_ascii': False})
    try:
        object1.save()
    except:
        return JsonResponse({'code': -1, 'errorMsg': '已经存在，请勿新增'},
                           json_dumps_params={'ensure_ascii': False})

    return rsp
# 新增区域的1个接口

def insertCountry(request):
    first = request.POST["first"]
    two = request.POST['two']
    three = request.POST['three']
    four = request.POST['four']
    rsp = JsonResponse({'code': 0, 'errorMsg': '增加成功'},
                           json_dumps_params={'ensure_ascii': False})
    if len(first) <=0 or len(two)<=0:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请填写地域名称'},
                           json_dumps_params={'ensure_ascii': False})
        return rsp
    # object = Country.objects.get(first=first, two=two)
    # if len(object) >= 1:
    #     rsp = JsonResponse({'code': 0, 'errorMsg': '该区域已经存在'},
    #                        json_dumps_params={'ensure_ascii': False})
    #     return rsp
    # else:
    object1 = Country(first = first, two = two, three = three, four = four)
    try:
        object1.save()
    except:
        return JsonResponse({'code': -1, 'errorMsg': '已经存在，请勿新增'},
                           json_dumps_params={'ensure_ascii': False})

    return rsp

# 获取区域列表的接口
# 管理员账号判断的接口， 账号密码判断给我
def verify(request):
    name = request.POST["name"]
    password = request.POST["password"]
    try:
        data = User.objects.get(name=name)
    except:
        return JsonResponse({'code': -1, 'errorMsg': '用户名不对'},
                    json_dumps_params={'ensure_ascii': False})

    password1 = data.password
    if password == password1:
        return JsonResponse({'code': 0, 'data': 0},
                           json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': '密码不对'},
                            json_dumps_params={'ensure_ascii': False})
# 核算记录插入接口
def insertHistory(request):
    name = request.POST['name']
    sex = request.POST['sex']
    age = request.POST['age']
    birth = request.POST['birth']
    idcard = request.POST['idcard']
    iphone = request.POST['iphone']
    addtime = time.strftime("%Y-%m-%d", time.localtime())
    times = request.POST['times']
    userid = request.POST['userid']
    object = History(name=name, sex = sex, age = age, birth = birth, idcard = idcard, iphone = iphone, addtime = addtime, times = times, userid = userid)
    try:
        object.save()
    except:
        return JsonResponse({'code': -1, 'errorMsg': '请勿重复新增'},
                           json_dumps_params={'ensure_ascii': False})
    rsp = JsonResponse({'code': 0, 'errorMsg': '增加成功'},
                       json_dumps_params={'ensure_ascii': False})
    return  rsp
# 判断某人是第几次核酸接口， 根据身份证去查
def getHistory(request):
    idcard = request.POST['idcard']
    key = "^[1-9]{2}\d{4}(18|19|20)\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
    brea = re.match(key, idcard)
    if brea != None:
        try:
            data = History.objects.get(idcard = idcard)
            times = len(data) + 1
            return JsonResponse({'code': 0, 'data': times},
                                json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({'code': -1, 'errorMsg': '获取失败'},
                                json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': -1, 'errorMsg': '身份证不合法'},
                        json_dumps_params={'ensure_ascii': False})
# 识别身份证
def shibie(request):
    image = request.POST['image']
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    def get_token(client_id,client_secret):
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        grant_type = "client_credentials"
        resp = requests.post(url=token_url,data={'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret},headers={'Content-Type':'application/x-www-form-urlencoded'})
        resp = resp.json()
        return resp['access_token']
    image = get_file_content('/Users/didi/Desktop/WechatIMG151.jpeg')
    image = base64.b64encode(image)
    #print(image)
    # image = str(base64.b64decode(image), "utf-8")
    APP_ID = '25850679'
    API_KEY = 'rT7pLyZ0H0FfFVoxvehgi2YY'
    SECRET_KEY = 'YIj9WYQ0mZiBfz576gIV13xbOuL14ujI'
    # client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # idCardSide = "front"
    # res_image = client.idcard(image, idCardSide)
    params = {"id_card_side": "front", "image": image}
    access_token = get_token(API_KEY,SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        return JsonResponse({'code': 0, 'data': response.json()},
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg':"识别错误"},
                        json_dumps_params={'ensure_ascii': False})
# 提供excel 文件下载

def  download(request):
    diff_times1 = int(request.POST['diff_times1'])
    diff_times2 = int(request.POST['diff_times2'])
    # diff_data1 = History.objects.get(times = diff_times1)
    # diff_data2 = History.objects.get(times = diff_times2)

    sql = 'select * from wxcloudrun_history where times=%d and idcard not in (select idcard from wxcloudrun_history where times = %d)'%(diff_times1, diff_times2)
    command = 'sh %s/output.sh %d %d'%(os.path.abspath('.'),diff_times1,diff_times2)
    print(command)
    val = os.system(command)
    print(val)
    return JsonResponse({'code': -1, 'errorMsg': '身份证不合法'},
                        json_dumps_params={'ensure_ascii': False})
    # 拼装sql 语句

    # try:
    #     ret =History.objects.raw(sql)
    # except:
    #     return JsonResponse({'code': -1, 'errorMsg': '下载失败'},
    #                         json_dumps_params={'ensure_ascii': False})
    # print(type(ret))
    # for book in ret:
    #     print(book.name)


    # if len(ret) >= 1 :
    #     output = "aa.excel"
    #     data = pd.DataFrame(ret)
    #     data.columns(['记录id','姓名', '性别', '年龄', '出生日期', '身份证信息', '手机号', '核算时间', '核算次数', "管理员id"])  # 设置excel表头
    #     output = io.BytesIO()  # 配置一个BytesIO 这个是为了转二进制流
    #     data.to_excel(output, index=False)  # index=False 是为了不建立索引
    #     output.seek(0)  # 把游标归0
    #     return  output
    # else:
    #     return JsonResponse({'code': 0,'errorMsg': '本轮已全部做核算'},
    #                         json_dumps_params={'ensure_ascii': False})


