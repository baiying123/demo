from django.contrib import admin

from goods.models import (Category,
                          Unit,
                          GoodsSPU,
                          GoodsSKU,
                          Gallery,
                          ActivityZone,
                          Banner,
                          Activity,
                          )

"""
注册方式:
admin.site.register(模型类)

装饰器形式注册
@admin.register(模型类)
class XxxAdmin(admin.ModelAdmin):
    # 自定义后显示的类
"""

# 商品分类
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 4
    # 自定义后台
    # 指定显示的列
    list_display = ['id', 'sort_name', 'intro', 'order', 'update_time']
    # 设置可编辑连接字段
    list_display_links = ['id', 'sort_name', 'intro']

# 商品SKU_单位
admin.site.register(Unit)
# 商品SKU表
admin.site.register(GoodsSPU)


# 商品sku
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 2


@admin.register(GoodsSKU)
class GoodsSkuAdmin(admin.ModelAdmin):
    list_display = ["id", 'sku_name', 'price', 'unit', 'Store', 'sale_num', 'is_on_sale', 'category']
    list_display_links = ["id", 'sku_name', 'price']

    search_fields = ['sku_name', 'price', 'sale_num']
    inlines = [
        GalleryInline,
    ]


# 首页轮播
admin.site.register(Banner)
# 首页活动
admin.site.register(Activity)

# 首页活动专区
@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 4
    # 自定义后台
    # 指定显示的列
    list_display = ['id', 'title', 'intro', 'order', 'is_on_sale']
    # 设置可编辑连接字段
    list_display_links = ['id', 'title', 'intro', 'order', 'is_on_sale']