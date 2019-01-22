from django.conf.urls import url

from user.views import RegisterView, LoginView, MemberView, InforView, PasswordView, SaftystepView, ForgetpasswordView, \
    SendMsm

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name="注册"),
    url(r'^login/$', LoginView.as_view(), name="登录"),
    url(r'^member/$', MemberView.as_view(), name="个人中心"),
    url(r'^infor/$', InforView.as_view(), name="个人资料"),
    url(r'^saftystep/$', SaftystepView.as_view(), name="安全设置"),
    url(r'^password/$', PasswordView.as_view(), name="修改密码"),
    url(r'^forgetpassword/$', ForgetpasswordView.as_view(), name="修改密码"),
    url(r'^sendMsm/$',SendMsm.as_view(), name="发送短信验证"),

]