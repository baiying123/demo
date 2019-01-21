from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, InforModelForm
from user.helper import set_password, login

from user.models import Users


class RegisterView(View):  # 注册
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
            #获取清洗后的数据
            cleaned_data = form.cleaned_data
            #保存数据库
            user = Users()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            return redirect('user:登录')
        else:
            return render(request, 'user/reg.html', context={'form': form})


class LoginView(View):  # 登录
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = LoginModelForm(data)
        if form.is_valid():
            # 验证成功
            #保存登录标识到session中，单独创建一个方法保存，更新个人资料
            user = form.cleaned_data.get('user')
            login(request,user)#保存session

            # 合成响应跳转到个体中心
            return redirect('user:个人中心')
        else:
            # 提示错误，重新登录
            return render(request, 'user/login.html', {'form': form})


class MemberView(VerifyLoginView):  # 个人中心,基础验证是否登录的视图

    def get(self,request):
        return render(request,'user/member.html')
    def post(self,request):
        return render(request, )
# @check_login
# def xxx(request):#视图函数
#     pass

class InforView(VerifyLoginView):#个人资料
    def get(self,request):
        return render(request,'user/infor.html')
    def post(self,request):
        data = request.POST

        # 验证数据的合法性
        form = InforModelForm(data)

        if form.is_valid():
            #获取清洗后的数据
            cleaned_data = form.cleaned_data
            #保存数据库
            user = Users()
            user.my_birthday = cleaned_data.get('my_birthday')
            user.save()
            user = form.cleaned_data.get('user')
            login(request, user)  # 保存session

              # 保存session

            # 合成响应跳转到个体中心
            return redirect('user:个人中心')
        else:
            # 提示错误，重新登录
            return render(request, 'user/infor.html', {'form': form})
class SaftystepView(VerifyLoginView):#安全设置
    def get(self,request):
        return render(request,'user/saftystep.html')
    def post(self,request):
        pass
class PasswordView(VerifyLoginView):
    def get(self,request):
        return render(request,'user/saftystep.html')
    def post(self,request):
        pass