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
from wxcloudrun.models import Alluser
import pandas as pd   # 导入pandas 并重命名 pd
import io
import datetime
import traceback
# from aip import AipOcr
import requests
requests.adapters.DEFAULT_RETRIES = 3
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger('log')
FILE_PATH = "/usr/local/nginx/files/"


def getuser(request):
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    try:
        data = User.objects.get(name="liuwenrui")
    except User.DoesNotExist:
        response = JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
        response['Access-Control-Allow-Origin'] = '*'  # 允许的跨域名
        response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
        response['Access-Control-Allow-Method'] = '*'  # 允许的请求方法
        return response
    response = JsonResponse({'code': 0, 'data': data.name},
                        json_dumps_params={'ensure_ascii': False})
    response['Access-Control-Allow-Origin'] = '*'  # 允许的跨域名
    response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
    response['Access-Control-Allow-Method'] = '*'  # 允许的请求方法
    return response
def getalluser(request):
    # sql = "select * from wxcloudrun_user where role = 2"
    try:
        data = User.objects.filter(role=2)
        return_list = []
        for item in data:
            temp = [item.name, item.password, item.area]
            return_list.append(temp)
        return JsonResponse({'code': 0, 'data': return_list},
                    json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 0, 'data': ""},
                     json_dumps_params={'ensure_ascii': False})
def insertUser(request):
    area = request.POST['area']
    name = request.POST['name']
    password = request.POST['password']
    object1 = User(name = name,password = password, role = 2, area = area)
    rsp = JsonResponse({'code': 0, 'data': 0},
                       json_dumps_params={'ensure_ascii': False})
    try:
        object1.save()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': -1, 'errorMsg': '已经存在，请勿新增'},
                           json_dumps_params={'ensure_ascii': False})

    return rsp
# 新增区域的1个接口

def insertCountry(request):
    first = request.POST["first"]
    two = request.POST['two']
    three = request.POST['three']
    # four = request.POST['four']
    rsp = JsonResponse({'code': 0, 'errorMsg': '增加成功'},
                           json_dumps_params={'ensure_ascii': False})
    # object = Country.objects.get(first=first, two=two)
    # if len(object) >= 1:
    #     rsp = JsonResponse({'code': 0, 'errorMsg': '该区域已经存在'},
    #                        json_dumps_params={'ensure_ascii': False})
    #     return rsp
    # else:
    object1 = Country(first = first, two = two, three = three)
    try:
        object1.save()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': -1, 'errorMsg': '已经存在，请勿新增'},
                           json_dumps_params={'ensure_ascii': False})

    return rsp

# 拿所有的从村 或者 社区 到小区 到 组的关系
def getAllContent(request):
    # 获取所有的村或者社区
    response_dict = {}
    #sql = "select distinct(first) from wxcloudrun_country"
    try:
         # ret = Country.objects.raw(sql)
        ret = Country.objects.values('first').distinct()
        ret_2 = Country.objects.values('two').distinct()
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 0, 'data': ""},
                            json_dumps_params={'ensure_ascii': False})
    # 获取所有村名 or 社区，并初始化字典
    return_dict = {}
    return_zu_dict = {}
    cun_keys = set()
    xiaoqu_keys = set()
    for item in ret:
        cun = item['first']
        cun_keys.add(cun)
    for item in ret_2:
        xiaoqu_keys.add(item['two'])
    for item in cun_keys:
        return_dict[item]=[]
    for item in xiaoqu_keys:
        return_zu_dict[item]=[]
    # 根据小区 获取所有组号
    for item in ret_2:
        xiaoqu = item['two']
        try:
            object1 = Country.objects.filter(two = xiaoqu)
            for item in object1:
                return_zu_dict[xiaoqu].append(item.three)
            return_zu_dict[xiaoqu] = list(set(return_zu_dict[xiaoqu]))
        except Exception as e:
            traceback.print_exc()

    # 根据村名 获取所有的小区
    for item in ret:
        cun = item['first']
        try:
            object = Country.objects.filter(first = cun )
            for item in object:
                return_dict[cun].append(item.two)
            return_dict[cun] = list(set(return_dict[cun]))

        except Exception as e:
            traceback.print_exc()

    response_dict["xiaoqu_to_zu"] = return_zu_dict
    response_dict["cun_to_xiaoqu"] = return_dict
    return JsonResponse({'code': 0, 'data': response_dict},
                        json_dumps_params={'ensure_ascii': False})



# 获取村/社区下的所有小区
def getXiaoqu(request):
    cun = request.POST['cun']
    try:
        object = Country.objects.filter(first= cun)
        xiaoqu = []
        for item in object:
            xiaoqu.append(item.two)
    except:
        return JsonResponse({'code': 0, 'data': 0},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': xiaoqu},
                            json_dumps_params={'ensure_ascii': False})


def getCun(request):
    all_cun = []
    try:

        ret = Country.objects.values('first').distinct()
        for item in ret:
           cun = item['first']
           all_cun.append(cun)
    except:
        return JsonResponse({'code': 0, 'data': 0},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': all_cun},
                            json_dumps_params={'ensure_ascii': False})


# 根据已有的身份证号获取电话
def getiphone(request):
    idcard = request.POST['idcard']
    sql = "select * from wxcloudrun_history where idcard='%s' limit 1"%(idcard)
    print(sql)
    try:
        ret = History.objects.raw(sql)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'code': 0, 'data': ''},
                            json_dumps_params={'ensure_ascii': False})

    if ret:
        for item in ret:
            iphone = item.iphone
        return JsonResponse({'code': 0, 'data': iphone},
                        json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': 0, 'data': ''},
                            json_dumps_params={'ensure_ascii': False})
# 获取区域列表的接口
# 管理员账号判断的接口， 账号密码判断给我
def verify(request):
    name = request.POST["name"]
    password = request.POST["password"]
    first = request.POST['first']
    try:
        data = User.objects.get(name=name)
    except:
        return JsonResponse({'code': -1, 'errorMsg': '用户名不对'},
                    json_dumps_params={'ensure_ascii': False})

    password1 = data.password
    area = data.area
    role = data.role
    if password == password1:
        if first != area and role!=1:
            return JsonResponse({'code': -1, 'errorMsg': '您非本区域管理员'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'code': 0, 'data': {"role": data.role, "userid":data.id}},
                           json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': '密码不对'},
                            json_dumps_params={'ensure_ascii': False})


# 核算记录插入接口
def insertHistory(request):
    name = str(request.POST['name'])
    sex = str(request.POST['sex'])
    age = request.POST['age']
    birth = request.POST['birth']
    birth = datetime.datetime.strptime(birth,'%Y-%m-%d')
    idcard = request.POST['idcard']
    iphone = request.POST['iphone']
    addtime = time.strftime("%Y-%m-%d", time.localtime())
    # times = request.POST['times']
    # 轮次
    times = int(request.POST['times'])
    # 常住地
    first = str(request.POST['first'])
    two = str(request.POST['two'])
    userid = request.POST['userid']
    #userid = 22
    # area = request.POST["area"]
    # 给alluser 表新增记录
    object = History(name=name, sex = sex, age = age, birth = birth, idcard = idcard, iphone = iphone, addtime = addtime, times = times, area = first, two = two,  userid = userid)
    object1 = Alluser(idcard = idcard, first= first, two = two)
    try:
        object1.save()
    except Exception as e:
        traceback.print_exc()
    try:
        object.save()
    except Exception as e:
        traceback.print_exc()
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
    # image = get_file_content('/Users/didi/Desktop/WechatIMG151.jpeg')
    # image = base64.b64encode(image)
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
        res_json = response.json()
        if res_json['image_status'] == "normal":
            name = res_json['words_result']['姓名']['words']
            idcard = res_json['words_result']['公民身份号码']['words']
            birth = res_json['words_result']['出生']['words']
            sex = res_json['words_result']['性别']['words']
            return_res = {"name":name, "idcard":idcard,"birth":birth,"sex":sex}
            res_json = JsonResponse({'code': 0, 'data': return_res},
                                json_dumps_params={'ensure_ascii': False})
            res_json['Access-Control-Allow-Origin'] = '*'  # 允许的跨域名
            res_json['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
            res_json['Access-Control-Allow-Method'] = '*'  # 允许的请求方法
            return  res_json
        else:
            res_json =  JsonResponse({'code': -1, 'errorMsg': "图片错误"},
                                json_dumps_params={'ensure_ascii': False})
            res_json['Access-Control-Allow-Origin'] = '*'  # 允许的跨域名
            res_json['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
            res_json['Access-Control-Allow-Method'] = '*'  # 允许的请求方法
            return res_json
    else:
        res_json=JsonResponse({'code': -1, 'errorMsg':"识别错误"},
                        json_dumps_params={'ensure_ascii': False})
        res_json['Access-Control-Allow-Origin'] = '*'  # 允许的跨域名
        res_json['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
        res_json['Access-Control-Allow-Method'] = '*'  # 允许的请求方法
        return res_json
# 提供文件下载

def  download(request):
    # 输入的轮次
    times = int(request.POST['times'])
    # 输入区域
    cun = request.POST['cun']
    #download_file = "down.xlsx"
    file_name = "down_%d.xlsx"%(times)

    download_file = FILE_PATH + file_name
    download_url = "http://81.70.239.81/files/"+file_name
    if times is None:
        return JsonResponse({'code': -1, 'errorMsg': '请输入轮次'},
                         json_dumps_params={'ensure_ascii': False})

    # 本轮所选区域本轮次未做核算人次
    if cun is None or cun == "全部":
        # 本轮未做核算人次
        sql = "select * from wxcloudrun_alluser where idcard not in(select idcard from wxcloudrun_history where times=%d)" % (
            times)
        # 查询本轮应该做多少
        sql1 = "select * from wxcloudrun_alluser"
        # 本轮已做核算人数

        # sql3 = "select * from wxcloudrun_history where times=%d"%(times)
        # 本轮包含外部人员多少？
        sql2 = "select id, idcard from wxcloudrun_history where times=%d and area != '%s'" % (times, cun)
    else:
        sql = "select * from wxcloudrun_history where area='%s' and idcard not in(select idcard from wxcloudrun_history where times=%d)" % (
            cun,times)
        #查询本轮应该做多少
        sql1 = "select * from wxcloudrun_alluser where first ='%s'"%(cun)
        # 本轮包含外部人员多少？
        sql2 = "select * from wxcloudrun_history where times=%d and area != '%s' and idcard in (select idcard from wxcloudrun_alluser where first = '%s')" % (times, cun,cun)

        # sql3 = "select * from wxcloudrun_history where times=%d and area ='%s'"%(times,cun)
    print(sql)
    print(sql1)
    print(sql2)
    data_list = []
    sql1_data_list = []
    sql2_data_list = []
    # sql3_data_list = []
    try:
        object2 = History.objects.raw(sql)
        for obj in object2:
            data = []  # 要在遍历里面创建字典用于存数据
            print(obj)
            data.append(obj.name)
            data.append(obj.sex)
            data.append(obj.age)
            data.append(obj.idcard)
            data.append(obj.iphone)
            data.append(obj.area)
            data_list.append(data)

        # sql3_object = History.objects.raw(sql3)
    except:
        traceback.print_exc()
    try:
        sql1_object = Alluser.objects.raw(sql1)
        for obj in sql1_object:
            data = []
            data.append(obj.idcard)
            data.append(obj.first)
            sql1_data_list.append(data)
    except:
        traceback.print_exc()
        # for obj in sql3_object:
        #     data = []  # 要在遍历里面创建字典用于存数据
        #     print(obj)
        #     data.append(obj.name)
        #     data.append(obj.sex)
        #     data.append(obj.age)
        #     data.append(obj.idcard)
        #     data.append(obj.iphone)
        #     data.append(obj.area)
        #     sql3_data_list.append(data)
    try:
        sql2_object = History.objects.raw(sql2)
        for obj in sql2_object:
            data = []
            data.append(obj.idcard)
            sql2_data_list.append(data)
    except:
        traceback.print_exc()

    # 本轮未做核算人数
    not_hesuan_count = len(data_list)
    # 本轮已做核算人数
    not_hesuan_data = None
    done_cun_data = None
    if len(data_list)>0:
        not_hesuan_data = pd.DataFrame(data_list, columns=['姓名', '性别', '年龄', '身份证信息', '手机号', "所属区域"])
        # data.to_excel("aa.xlsx", index=False,sheet_name="本轮未做核算")  # index=False 是为了不建立索引

    # 这个区域本轮已做核算人数
    if cun is None or cun == "全部":
        object1 = History.objects.filter(times=times).values_list("name","sex", "age","idcard","iphone","area")
    else:
        object1 = History.objects.filter(times=times, area=cun).values_list("name", "sex", "age", "idcard", "iphone", "area")
    object1 = list(object1)
    done_cun_count = len(object1)
    if len(object1) >= 1 :
        done_cun_data = pd.DataFrame(object1, columns=['姓名', '性别', '年龄', '身份证信息', '手机号', "所属区域"])
        # data.to_excel("aa.xlsx", index=False, sheet_name="本区域本轮已做核算人数")  # index=False 是为了不建立索引
    if len(data_list) > 0 and len(object1) > 0:
        with pd.ExcelWriter(download_file) as writer:
            not_hesuan_data.to_excel(writer, sheet_name='本轮未做核酸', index=False)
            done_cun_data.to_excel(writer, sheet_name='本轮已做核酸', index=False)
    elif len(data_list) >0 and len(object1) <=0:
        with pd.ExcelWriter(download_file) as writer:
            not_hesuan_data.to_excel(writer, sheet_name='本轮未做核酸', index=False)
    elif len(data_list) <=0 and len(object1) >0:
        with pd.ExcelWriter(download_file) as writer:
            done_cun_data.to_excel(writer, sheet_name='本轮已做核酸', index=False)
    # 这个区域以外本轮在这边已做核算人次
    not_area_count = len(sql2_data_list)
    # 这个区域本来应该做多少人
    should_count = len(sql1_data_list)
    # 这个区域做了多少？
    area_count = done_cun_count - not_area_count
    return JsonResponse({'code': 0, 'data': {"should_count":should_count,"not_hesuan_count":not_hesuan_count, "done_cun_count":done_cun_count, "not_area_count":not_area_count, "area_count":area_count, "fileurl":download_url}},
                            json_dumps_params={'ensure_ascii': False})





