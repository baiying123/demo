from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.



from car.helper import get_car_count
from goods.models import GoodsSKU, Category

# 商品首页
class IndexView(View):
    def get(self, request):
        a = GoodsSKU.objects.filter(is_delete=False)
        b = Category.objects.filter(is_delete=False)
        context = {
            'a': a,
            'b': b
        }
        return render(request, 'goods/index.html', context=context)


# 商品分类(商品列表)
class CategorView(View):
    def get(self, request, cate_id,order):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False).order_by("-order")
        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据分类id查询对应的分类
            cate_id = int(cate_id)
            # category = Category.objects.filter(pk=cate_id)
            # goods_skus = GoodsSKU.objects.filter(is_delete=False, category=category)
            cate_id = int(cate_id)
            category = Category.objects.get(pk=cate_id)
        goods_skus = GoodsSKU.objects.filter(is_delete=False, category=category)

        if order == "":
            order = 0
        order = int(order)
        order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        goods_skus = goods_skus.order_by(order_rule[order])
        # if order == "":
        #     order = 0
        # order = int(order)
        #
        # # 排序规则列表
        # order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        # goods_skus = goods_skus.order_by(order_rule[order])
        # 获取 当前用户 购物车中商品的总数量
        car_count = get_car_count(request)

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
            'cate_id': cate_id,
            'order': order,
            'car_count': car_count,
        }

        return render(request, 'goods/category.html', context=context)


# 商品详情
class DetailView(View):
    def get(self, request, id):
        # 获取商品sku的信息
        goods_sku = GoodsSKU.objects.get(pk=id)

        # 渲染页面
        context = {
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)
