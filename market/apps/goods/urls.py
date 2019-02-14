from django.conf.urls import url
from django.views.generic import edit

from goods.views import DetailView, CategorView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='首页'),
    url(r'^list/(?P<cate_id>\d*)_{1}(?P<order>\d?)\.html$', CategorView.as_view(), name='分类列表'),

    url(r'^detail/(?P<id>\d+)/$', DetailView.as_view(), name="商品详情"),

]
