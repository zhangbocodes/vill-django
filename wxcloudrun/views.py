import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters
from wxcloudrun.models import User
from wxcloudrun.models import History
from wxcloudrun.models import Country

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
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
# 核算记录插入接口

# 判断某人是第几次核酸接口， 根据身份证去查



def counter(request):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
