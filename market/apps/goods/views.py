from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.


# 商品首页
class Index(View):
    def get(self, request):
        return render(request, 'goods/index.html')
    def post(self,request):
        return HttpResponse('商品首页post')



# 商品分类(商品列表)
class Category(View):
    def get(self, request):
        return render(request, 'goods/category.html')
    def post(self,request):
        return HttpResponse('商品分类post')



# 商品详情
class Detail(View):
    def get(self, request):
        return render(request, 'goods/detail.html')
    def post(self,request):
        return HttpResponse('商品分类post')

