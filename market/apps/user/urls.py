from django.conf.urls import url

from user.views import IndexView, LoginView, RegisterView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name="注册"),
    url(r'^login/$', LoginView.as_view(), name="登录"),
    url(r'^index/$', IndexView.as_view, name="首页"),

]