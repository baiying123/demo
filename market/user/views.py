from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from user import set_password
from user.forms import RegisterModelForm, LoginModelForm
from user.models import Users


class RegisterView(View):#注册
    template_name = 'user/reg.html'

    def get(self, request):
        # 展示登录表单
        return render(request, self.template_name)

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        data = request.POST
        # 验证参数合法性 表单验证
        form = RegisterModelForm(data)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = Users()
            user.username = cleaned_data.get('username')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            return redirect('user:登录')
        else:
            return render(request, self.template_name, context={'form': form})


class LoginView(View):  # 登录
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = LoginModelForm(data)
        if form.is_valid():
            # 验证成功 session
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['username'] = user.username
            # 操作数据库
            return redirect('user:首页')
        else:
            # 合成响应
            return render(request, 'user/login.html', {'form': form})
