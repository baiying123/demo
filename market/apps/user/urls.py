from django.conf.urls import url

from user.views import RegisterView, LoginView, MemberView, InforView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name="注册"),
    url(r'^login/$', LoginView.as_view(), name="登录"),
    url(r'^member/$', MemberView.as_view, name="个人中心"),
    url(r'^infor/$', InforView.as_view, name="个人资料"),

]