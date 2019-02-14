from datetime import date

# 注册ModelForm的模型类
from django.core import validators
from django.core.validators import RegexValidator
from django import forms

from user.helper import set_password
from user.models import Users, UserAddress


# 注册表单
class RegisterModelForm(forms.Form):
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
    repassword = forms.CharField(error_messages={
        'required': '确认密码必填',

    })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写"
                              })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议'
    })

    # 模型用的 Users
    class Meta:
        model = Users
        exclude = ['phone', 'password', 'repassword']

    # 验证在数据库中 手机号是否存在
    def clean_phone(self):  # 验证手机号是否唯一
        phone = self.cleaned_data.get('phone')
        flag = Users.objects.filter(phone=phone).exists()
        if flag:
            # 在数据库中存在 提示错误
            raise forms.ValidationError("手机号码已被注册")

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
            raise forms.ValidationError({'password': '密码错误'})
        self.cleaned_data['user'] = user  # seesion返回整条记录
        return self.cleaned_data
        # 综合校验
        # 验证 用户传入的验证码和redis中的是否一样
        # 用户传入的
        try:
            captcha = self.cleaned_data.get('captcha')
            phone = self.cleaned_data.get('phone', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(phone)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})

        # 返回清洗后的所有数据
        return self.cleaned_data


# 个人资料表单
class InforModelForm(forms.Form):
    # 用户昵称
    my_name = forms.CharField(max_length=50,
                              min_length=2,
                              error_messages={
                                  'min_length': '用户昵称最小长度必须为2位',
                                  'max_length': '用户昵称最大长度不能超过50位',
                              })

    school = forms.CharField(max_length=50,
                             error_messages={
                                 'max_length': '学校最大长度不能超过50位'
                             })
    my_home = forms.CharField(max_length=50,
                              error_messages={
                                  'max_length': '用户详细地址位置最大长度不能超过50位'
                              })
    address = forms.CharField(max_length=50,
                              error_messages={
                                  'max_length': '用户的故乡最大长度不能超过50位'
                              })
    phone = forms.CharField(error_messages={
        "required": "手机号必填",
    },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
        ]
    )

    def clean_my_birthday(self):
        # 获取当前日期
        now_date = date.today()
        my_birthday = self.cleaned_data.get('my_birthday')
        # 比较大小
        if my_birthday > now_date:
            return forms.ValidationError('出生日期必须大于当前时间')
        return my_birthday

        # 模型用的 Users

    class Meta:
        model = Users
        fields = ['my_name', 'school', 'my_home', 'address', 'phone','my_birthday']
        # 提示错误信息
        error_messages = {
            "my_name": {
                'required': '用户昵称必须填写',
                'max_length': '用户昵称长度不能大于50',
                'min_length': '用户昵称最小长度必须为2位',
            },
            'school': {
                'max_length': '学校最大长度不能超过50位'
            },
            'my_home': {
                'max_length': '用户详细地址位置最大长度不能超过50位'
            },
            'address': {
                'max_length': '用户的故乡最大长度不能超过50位'
            },
            'tel': {
                'required': '手机号必须填写',
                'max_length': '手机号长度不能大于11',
            }
        }


# 修改密码
class PasswordModelForm(forms.Form):
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少八个字符!',
                                   'max_length': '请输入小于或等于十六个字符!'
                               })
    newpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必须填写新密码',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })
    renewpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必须填写密码',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })

    class Meta:
        model = Users




    # 验证密码是否一致
    def clean(self):
        # 判断两次密码是否一致
        # 在清洗的数据中的到表单提交的数据,密码和确认密码
        pwd = self.cleaned_data.get('newpassword')
        repwd = self.cleaned_data.get('renewpassword')
        if pwd and repwd and pwd != repwd:
            # 在密码和确认密码,并且确认密码和密码不一样的时候,提示错误信息
            raise forms.ValidationError({'renewpassword': "两次密码不一致"})
        else:
            return self.cleaned_data


# 忘记密码
class ForgetpasswordModelForm(forms.Form):
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
    newpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必须填写新密码',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })
    renewpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必填',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写!"
                              })
    class Meta:
        model = Users
        exclude = ['phone', 'password']

    def clean_phone(self):  # 验证是否存在
        phone = self.cleaned_data.get('phone')
        flag = Users.objects.filter(phone=phone).exists()
        if not flag:
            # 在数据库中不存在 提示错误
            raise forms.ValidationError("用户不存在")

        # 返回单个字段 ,不用返回全部
        return phone

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

#用户添加收货地址的表单"
class AddressAddForm(forms.ModelForm):
    """用户添加收货地址的表单"""
    class Meta:
        model = UserAddress
        exclude = ['create_time', 'update_time', 'is_delete','user']
        error_messages = {
            'username': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'brief': {
                'required': "请填写详细地址！",
            },
            'harea': {
                'required': "请填写完整地址！",
            },
        }

    def clean(self):
        # 验证如果数据库里地址已经超过6六表报错
        cleaned_data = self.cleaned_data
        count = UserAddress.objects.filter(user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"harea":"收货地址最多只能保存6条"})

        #操作默认值
        # 如果当前是默认地址,其他 就设置为False
        if cleaned_data.get('isDefault'):
            UserAddress.objects.filter(user_id=self.data.get("user_id")).update(isDefault=False)

        return cleaned_data