from django.db import models



# Create your models here.
from db.base_model import BaseModel


class Users(BaseModel):
    phone= models.CharField(max_length=50, verbose_name='用户名,使用手机号')
    password = models.CharField(max_length=32, verbose_name='密码')
    my_name = models.CharField(max_length=50, null=True,blank=True,verbose_name='用户昵称')#默认为空，可以不填注册
    gender_choices = (
        (1, '男'),
        (2, '女'),

    )
    sex = models.IntegerField(choices=gender_choices, default=1, verbose_name='性别选择,默认保密')
    my_birthday = models.DateField(blank=True, null=True,verbose_name='用户生日,默认为空')
    school = models.CharField(max_length=50,blank=True, null=True,verbose_name='学校')#默认为空，可以不填
    my_home = models.CharField(max_length=50,blank=True, null=True,verbose_name='用户详细地址位置')
    address = models.CharField(max_length=50,blank=True, null=True,verbose_name='用户的故乡')
    #tel = models.CharField(max_length=11,null=True,blank=True, verbose_name='电话号码')
    # is_delete=models.BooleanField(default=False)#假删除
    # add_time=models.DateField(auto_now_add=True)#添加时间
    # update_time=models.DateField(auto_now=True)#修改时间
    # 用户头像从setting文件直接找到静态文件的储存路径
    head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")
    def __str__(self):
        return self.phone

    class Meta:
        db_table = "s_user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
