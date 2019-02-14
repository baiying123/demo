import random
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from market.settings import SECRET_KEY
from django.utils.decorators import method_decorator

from django.views import View
from django_redis import get_redis_connection

from car.helper import json_msg
from db.base_view import VerifyLoginView

from user.forms import RegisterModelForm, LoginModelForm, PasswordModelForm, ForgetpasswordModelForm, InforModelForm, \
    AddressAddForm
from user.helper import set_password, login, send_sms, check_login

from user.models import Users, UserAddress
import re

# 注册
class RegisterView(View):
    def get(self, request):
        # 展示登录表单
        return render(request, 'user/reg.html')

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        data = request.POST
        # 验证参数合法性 表单验证
        form = RegisterModelForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned_data = form.cleaned_data
            # 保存数据库
            user = Users()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            return redirect('user:登录')
        else:
            return render(request, 'user/reg.html', context={'form': form})

#发送短信验证
class SendMsm(View):
    def get(self, request):
        pass

    def post(self, request):
        # 1.接收参数
        phone = request.POST.get('phone')
        rs = re.search('^1[3-9]\d{9}$', phone)
        # 判断参数合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errmsg': '电话号码格式错误'})
        # 2处理数据
        # 模拟，最后接入运营商
        """1.生成随机验证码
            2.。。。。
            3接入运营商
        """
        # 1.生成随机验证码
        random_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        print('随机验证码为{}'.format(random_code))
        # 2保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(phone, random_code)
        r.expire(phone, 60)  # 设置60秒后过期
        # 首先获取当前手机号码的发送次数
        key_times = "{}_times".format(phone)
        now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # print(int(now_times))
        if now_times is None or int(now_times) < 5:
            # 保存手机发送验证码的次数, 不能超过5次
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 3600)  # 一个小时后再发送
        else:
            # 返回,告知用户发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多"})

        # 3 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"！！！！\"}" % random_code
        # print(params)
        rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 3. 合成响应
        return JsonResponse({'error': 0})

 # 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = LoginModelForm(data)
        if form.is_valid():
            # 验证成功
            # 保存登录标识到session中，单独创建一个方法保存，更新个人资料
            user = form.cleaned_data.get('user')
            login(request, user)  # 保存session
            referer = request.session.get('referer')
            if referer:
                # 跳转回去
                # 删除session
                del request.session['referer']
                return redirect(referer)
            else:
            # 合成响应跳转到个体中心
                return redirect('user:个人中心')
        else:
            # 提示错误，重新登录
            return render(request, 'user/login.html', {'form': form})

# 忘记密码
class ForgetpasswordView(View):
    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):

        # 接收参数
        data = request.POST
        # 验证参数合法性 表单验证
        form = ForgetpasswordModelForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 通过id查询数据
            user_id = request.session.get('ID')
            # 取出清洗后的手机号
            phone = cleaned.get('phone')
            # 取出清洗后的密码
            newpassword= set_password(cleaned.get('newpassword'))
            # 修改到数据库
            # 验证原密码是否存在,不能用get,用filter
            if Users.objects.filter(phone=phone, id=user_id).exists():
                # 更新密码
                Users.objects.filter(id=user_id).update(password=newpassword)
                # 跳转到登录页
                return redirect('user:登录')
        else:
            return render(request, 'user/forgetpassword.html', context={'form': form})

 # 个人中心,基础验证是否登录的视图
class MemberView(VerifyLoginView):

    def get(self, request):
        return render(request, 'user/member.html')

    def post(self, request):
        pass



# 个人资料
class InforView(VerifyLoginView):
    def get(self, request):
        # 获取session中的用户id
        user_id = request.session.get('ID')
        # 获取用户资料
        user = Users.objects.get(pk=user_id)
        context = {
            'user': user
        }
        return render(request, 'user/infor.html', context=context)


    def post(self, request):
        # 完成用户信息的更新
        # 接收参数
        # 渲染提交的数据
        data = request.POST
        head = request.FILES.get('head')
        user_id = request.session.get('ID')
        # 操作数据
        user = Users.objects.get(pk=user_id)
        user.my_name = data.get('my_name')
        user.sex = data.get('sex')
        user.birthday = data.get('birthday')
        user.school = data.get('school')
        user.my_home = data.get('my_home')
        user.address = data.get('address')
        if head is not None:
            user.head = head
        user.save()
        # 同时修改session
        login(request, user)
        # 合成响应
        return redirect('user:个人中心')

# 安全设置
class SaftystepView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/saftystep.html')

    def post(self, request):
        pass

# 修改密码
class PasswordView(VerifyLoginView):
    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        form = PasswordModelForm(data)
        # 验证数据的合法性
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后的密码
            # 将密码进行加密
            password = set_password(cleaned.get('password'))
            # 通过id查询数据
            user_id = request.session.get('ID')
            # print(user_id)
            # 修改到数据库
            # 验证原密码是否存在,不能用get,用filter
            if Users.objects.filter(id=user_id, password=password).exists():
                newpassword = set_password(cleaned.get('newpassword'))
                # 更新密码
                Users.objects.filter(id=user_id).update(password=newpassword)
                # 跳转到登录页
                return redirect('user:登录')


        else:
            # 提示错误
            return render(request, 'user/password.html', {'form': form})
#收货地址
class Address(VerifyLoginView):


    def get(self, request):
        return render(request, 'user/address.html')

    def post(self, request):
        # 接收参数
        data = request.POST.dict()  # 强制转换成字典

        # 字典保存用户
        data['user_id'] = request.session.get("ID")  # form自动转换功能

        # 验证参数
        form = AddressAddForm(data)
        if form.is_valid():
            form.instance.user = Users.objects.get(pk=data['user_id'])
            form.save()
            return JsonResponse(json_msg(0,"添加成功"))
        else:
            return JsonResponse(json_msg(1,"添加失败",data=form.errors))


class AddressList(VerifyLoginView):
    """收货地址列表"""

    def get(self, request):
        # 获取用户的收货地址
        user_id = request.session.get("ID")
        user_addresses = UserAddress.objects.filter(user_id=user_id,is_delete=False).order_by("-isDefault")


        # 渲染数据
        context = {
            'addresses':user_addresses
        }
        return render(request, 'user/address_list.html',context=context)
