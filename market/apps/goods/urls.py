from django.conf.urls import url

from goods.views import Category, Index, Detail

urlpatterns = [
    url(r'^index/$',Index.as_view(),name="商品首页"),
    url(r'^category/$',Category.as_view(),name="商品分类"),
    url(r'^detail/$',Detail.as_view(),name="商品详情"),


]