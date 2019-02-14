from django.conf.global_settings import SECRET_KEY
from django.http import JsonResponse
from django.shortcuts import redirect
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

import hashlib

from car.helper import json_msg
from market.settings import ACCESS_KEY_ID, ACCESS_KEY_SECRET


def set_password(password):
    # 循环加密 + 加盐
    for _ in range(1000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.md5(pass_str.encode('utf-8'))
        password = h.hexdigest()

    # 返回密码
    return password


# 将验证登录的方法写成装饰器
def check_login(func):  # 登录验证装饰器，传原函数
    def new_login(request, *args, **kwargs):
        #验证session中是否有登录标识
        if request.session.get("ID")is None:
            # 将上个请求地址保存到session
            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                request.session['referer'] = referer

            # 判断 是否为ajax请求
            #判断是否为ajax请求
            #跳转到登录页面
            if request.is_ajax():
                return JsonResponse(json_msg(1,'未登录'))
            else:
                #跳转到登录
                return redirect('user:登录')


        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return new_login


def login(request, user):  # 保存session的方法

    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session['head'] = user.head
    request.session.set_expiry(0)  # session存储时间，关闭浏览器就消失


# 完成 定义一个方法 发送短消
# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse
