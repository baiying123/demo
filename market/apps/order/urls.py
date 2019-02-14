from django.conf.urls import url

from order.views import ConfirmOrder, ShowOrder

urlpatterns = [
    url(r'^confirm/$', ConfirmOrder.as_view(), name='确认订单'),
    url(r'^order/$', ShowOrder.as_view(), name='确认支付'),
]
