"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from goods.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 用户模块
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    # 全文搜索框架
    url(r'^search/', include('haystack.urls', namespace='search')),
    url(r'^user/',include('user.urls',namespace='user')),
    url(r'^goods/',include('goods.urls',namespace='goods')),
    url(r'^$', IndexView.as_view()),
    url(r'^car/', include('car.urls', namespace='car')),
    url(r'^order/', include('order.urls', namespace='order')),
]
