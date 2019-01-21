from django.shortcuts import redirect

import hashlib

from market.settings import SECRET_KEY


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
        # 验证session中是否有登录标识
        if request.session.get('ID') is None:  # 没有
            # 跳转到登录
            return redirect('user:登录')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return new_login


def login(request, user):  # 保存session的方法

    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session.set_expiry(0)  # session存储时间，关闭浏览器就消失
