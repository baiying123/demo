
from datetime import date

from django import forms

from user import set_password
from user.models import Users


# 注册ModelForm的模型类
class RegisterModelForm(forms.ModelForm):
    # 单独定义一个字段
    # 密码
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })
    # 确认密码
    repassword = forms.CharField(max_length=16,
                                 min_length=8,
                                 error_messages={
                                     'required': '必须填写密码',
                                     'min_length': '密码最小长度必须为8位',
                                     'max_length': '密码最大长度不能超过16位',
                                 })

    # 模型用的 Users
    class Meta:
        model = Users
        fields = ['username']

        # 提示错误信息
        error_messages = {
            "username": {
                'required': '用户名必须填写',
                'max_length': '用户名长度不能大于11',
            }
        }

    # 验证在数据库中 用户名是否存在
    def clean_username(self):  # 验证用户名是否存在
        username = self.cleaned_data.get('username')
        flag = Users.objects.filter(username=username).exists()
        if flag:
            # 在数据库中存在 提示错误
            raise forms.ValidationError("该用户名已经存在,请重新填写")
        else:
            # 返回单个字段 ,不用返回全部
            return username

    # 验证密码是否一致
    def clean(self):
        # 判断两次密码是否一致
        # 在清洗的数据中的到表单提交的数据,密码和确认密码
        pwd = self.cleaned_data.get('password')  # ''
        repwd = self.cleaned_data.get('repassword')  # ''
        if pwd and repwd and pwd != repwd:
            # 在密码和确认密码,并且确认密码和密码不一样的时候,提示错误信息
            raise forms.ValidationError({'repassword': "两次密码不一致"})
        else:
            return self.cleaned_data


# 登录ModelForm的模型类
class LoginModelForm(forms.ModelForm):


    # 单独定义一个字段
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })

    class Meta:
        model = Users
        fields = ['username']

        # 提示错误信息
        error_messages = {
            "username": {
                'required': '用户名必须填写',
                'max_length': '用户名长度不能大于11',
            }
        }

    def clean(self):
        # 验证用户名
        username=self.cleaned_data.get('username')
        try:
            user=Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise forms.ValidationError({'username':'用户名错误'})
        password = self.cleaned_data.get('password', '')
        if user.password != set_password(password):#初始化加密密码
            raise forms.ValidationError({'password': '密码错误'})
        self.cleaned_data['user'] = user #seesion返回整条记录
        return self.cleaned_data

