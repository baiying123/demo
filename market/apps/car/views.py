from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

from car.helper import json_msg, get_car_count, get_car_key
from db.base_view import VerifyLoginView
from goods.models import GoodsSKU


# 操作购物车，添加购物车数据
class AddCarView(VerifyLoginView):
    def post(self, request):
        # 1接收参数

        # 需要接收的参数
        # sku_id
        # count
        # 从session中获取用户id
        user_id = request.session.get("ID")
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")
        # 2.验证参数合法性
        # a.判断为整数
        # b.要在数据库中存在商品
        # c.验证库存是否充足
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误!"))
        # b.要在数据库中存在商品
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在!"))
        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 3.操作数据库
        # 将购物车保存到redis存储的时候采用的数据库类型为hash
        # key           field  value  field value
        # cart_user_id  sku_id  count
        # 2. 操作数据
        # 创建连接
        r = get_redis_connection()
        # 处理购物车的 key
        car_key = get_car_key(user_id)

        # 添加
        # 获取购物车中已经存在的数量 加 上 需要添加 与 库存进行比较
        old_count = r.hget(car_key, sku_id)  # 二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 将商品添加到购物车
        # r.hset(cart_key,sku_id,old_count + count)
        # ctrl + shift + u
        rs_count = r.hincrby(car_key, sku_id, count)
        if rs_count <= 0:
            # 删除field
            r.hdel(car_key, sku_id)
        # 获取购物车中的总数量
        car_count = get_car_count(request)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=car_count))


# 购物车展示
class CarShowView(VerifyLoginView):
    """
    从redis获取所有的购物车信息(sku_id,count)
    根据购物中的sku_id从商品sku表中获取商品信息
    渲染的数据
     将购物车中的数量和商品信息合成一块
    """

    def get(self, request):
        # 接收参数
        user_id = request.session.get("ID")
        # 操作数据库
        r = get_redis_connection()
        # 准备键
        car_key = get_car_key(user_id)
        # 从redis获取所有的购物车信息(sku_id,count)
        car_datas = r.hgetall(car_key)
        # 准备空列表保存商品
        goods_skus = []

        # 遍历字典
        for sku_id, count in car_datas.items():
            # 将二进制转化成整型
            sku_id = int(sku_id)
            count = int(count)
            # 根据购物中的sku_id从商品sku表中获取商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                #删除redis中过期的数据
                r.hdel(car_key,sku_id)
                continue
                # 将购物车中的数量和商品信息合成一块
            goods_sku.count = count
                # setattr(goods_sku,'count',count)2种方法
        # 保存商品到商品列表
            goods_skus.append(goods_sku)
        # 渲染数据
        context = {
            'goods_skus': goods_skus
        }

        return render(request, 'car/shopcart.html',context=context)
