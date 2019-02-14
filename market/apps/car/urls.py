from django.conf.urls import url

from car.views import AddCarView,  CarShowView

urlpatterns = [
    url(r'^add/$',AddCarView.as_view(),name="添加购物车"),

    url(r'^list/$',CarShowView.as_view(),name="购物车展示"),
]
