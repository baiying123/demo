from django.conf.urls import url
from django.views.generic import edit

from goods.views import DetailView, CategorView

urlpatterns = [
    url(r'^list/$', CategorView.as_view(), name='分类列表'),

    url(r'^detail/(?P<id>\d+)$',DetailView.as_view(),name="商品详情"),


]