from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.


# 商品首页
from goods.models import GoodsSKU, Category


class Index(View):
    def get(self, request):
        return render(request, 'goods/index.html')
    def post(self,request):
        return HttpResponse('商品首页post')



# 商品分类(商品列表)
class CategorView(View):
    def get(self, request):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False)
        # 查询所有的商品
        goods_skus = GoodsSKU.objects.filter(is_delete=False)


        context = {
            'categorys':categorys,
            'goods_skus':goods_skus,
        }

        return render(request, 'goods/category.html',context=context)



# 商品详情
class DetailView(View):
    def get(self, request):
     goods_sku=GoodsSKU.objects.get(pk=id)
     context={
         'goods_sku':goods_sku
     }
     return render(request, 'goods/detail.html',context=context)
    def post(self,request):
        return HttpResponse('商品分类post')


