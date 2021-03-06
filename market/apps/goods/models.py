from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel
from django.conf import settings

is_on_sale_choices = (
    (False, "下架"),
    (True, "上架"),
)


# 商品spu表
class GoodsSPU(BaseModel):
    spu_name = models.CharField(verbose_name='商品SPU名称',
                                max_length=20)
    details = RichTextUploadingField(verbose_name='商品详情')

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


# 商品分类
class Category(BaseModel):
    sort_name = models.CharField(verbose_name='分类名',
                                 max_length=20
                                 )
    intro = models.CharField(verbose_name='简介',
                             max_length=200,
                             null=True,
                             blank=True
                             )
    order = models.SmallIntegerField(default=0, verbose_name="排序")

    def __str__(self):
        return self.sort_name

    class Meta:
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name


# 商品SKU_单位
class Unit(BaseModel):
    unit_name = models.CharField(max_length=20,
                                 verbose_name="单位")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "商品单位管理"
        verbose_name_plural = verbose_name


# 商品SKU表
class GoodsSKU(BaseModel):
    sku_name = models.CharField(verbose_name='商品SKU名称',
                                max_length=100,
                                )
    intro = models.CharField(verbose_name="商品的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    price = models.DecimalField(verbose_name='价格',
                                max_digits=9,
                                decimal_places=2,
                                default=0,
                                )
    unit = models.ForeignKey(to="Unit", verbose_name="单位")

    Store = models.IntegerField(verbose_name='库存',
                                default=0)

    sale_num = models.IntegerField(verbose_name='销量',
                                   default=0)

    # 默认相册中的第一张图片作为封面图片
    logo = models.ImageField(verbose_name='封面图片',
                             upload_to='goods/%Y%m/%d'
                             )

    def show_logo(self):
        return "<img style='width:100px' src='{}{}'/>".format(settings.MEDIA_URL, self.logo)

    show_logo.short_description = "LOGO"
    show_logo.allow_tags = True

    is_on_sale = models.BooleanField(verbose_name="是否上架",
                                     choices=is_on_sale_choices,
                                     default=False)

    category = models.ForeignKey(to="Category",
                                 verbose_name='商品分类'
                                 )

    goods_spu = models.ForeignKey(to="GoodsSPU", verbose_name="商品SPU")

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = "商品SKU管理"
        verbose_name_plural = verbose_name


# 商品相册
class Gallery(BaseModel):
    img_url = models.ImageField(verbose_name='相册图片地址',
                                upload_to='goods_gallery/%Y%m/%d'
                                )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品相册:{}".format(self.img_url.name)


# 首页轮播
class Banner(BaseModel):
    name = models.CharField(verbose_name="轮播活动名",
                            max_length=150,
                            )
    img_url = models.ImageField(verbose_name='轮播图片地址',
                                upload_to='banner/%Y%m/%d'
                                )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        verbose_name = "轮播管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页活动
class Activity(BaseModel):
    title = models.CharField(verbose_name='活动名称', max_length=150)
    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d'
                                )
    url_site = models.URLField(verbose_name='活动的url地址', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name


# 首页活动专区
class ActivityZone(BaseModel):
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    intro = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )
    is_on_sale = models.BooleanField(verbose_name="上否上线",
                                     choices=is_on_sale_choices,
                                     default=0,
                                     )
    goods_sku = models.ManyToManyField(to="GoodsSKU", verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name
