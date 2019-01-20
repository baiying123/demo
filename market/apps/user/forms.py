from datetime import date



# 注册ModelForm的模型类
from django.core import validators
from django.core.validators import RegexValidator
from django import forms

from user import set_password
from user.models import Users


class RegisterModelForm(forms.Form):#注册表单
    # 单独定义一个字段
    # 密码
    phone = forms.CharField(max_length=11,
                               min_length=11,
                               error_messages={
                                   'required': '必须填写手机号',
                                   'min_length': '手机号长度不能小于11',
                                   'max_length': '手机号长度不能大于11',
                               },
                                validators=[
                                    RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                                ]
                                )
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
                                     'required': '必须填写确认密码',
                                     'min_length': '密码最小长度必须为8位',
                                     'max_length': '密码最大长度不能超过16位',
                                 })

    # 模型用的 Users
    class Meta:
        model = Users
        exclude = ['phone', 'password', 'repassword']

    # 验证在数据库中 手机号是否存在
    def clean_username(self):  # 验证手机号是否存在
        phone = self.cleaned_data.get('phone')
        flag = Users.objects.filter(phone=phone).exists()
        if flag:
            # 在数据库中存在 提示错误
            raise forms.ValidationError("手机号码已被注册")
        else:
            # 返回单个字段 ,不用返回全部
            return phone

    # 验证密码是否一致
    def clean(self):
        # 判断两次密码是否一致
        # 在清洗的数据中的到表单提交的数据,密码和确认密码
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            # 在密码和确认密码,并且确认密码和密码不一样的时候,提示错误信息
            raise forms.ValidationError({'repassword': "两次密码不一致"})
        else:
            return self.cleaned_data


# 登录ModelForm的模型类
class LoginModelForm(forms.Form):
    # 单独定义一个字段
    phone = forms.CharField(max_length=11,
                               min_length=11,
                               error_messages={
                                   'required': '必须填写手机号',
                                   'min_length': '手机号长度不能小于11',
                                   'max_length': '手机号长度不能大于11',
                               },
                               validators=[
                                   RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                               ]
                               )
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })

    class Meta:
        model = Users
        exclude = ['phone', 'password']



    def clean(self):
        # 验证用户名
        phone = self.cleaned_data.get('phone')
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            raise forms.ValidationError({'phone': '手机号错误'})
        password = self.cleaned_data.get('password', '')
        if user.password != set_password(password):  # 初始化加密密码
            raise forms.ValidationError({'password': '两次密码不一致'})
        self.cleaned_data['user'] = user  # seesion返回整条记录
        return self.cleaned_data
