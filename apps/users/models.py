from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):  # 继承Django自身的AbstractUser,沿用默认字段
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")  # 增加昵称字段, 默认为空""
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)  # 增加生日字段, 允许null与空
    gender = models.CharField(choices=(("Male", "男"), ("female", "女")), max_length=6)  # 增加性别字段, 使用了choices选项
    address = models.CharField(max_length=100, default="")  # 增加地址字段
    mobile = models.CharField(max_length=11, null=True, blank=True)  # 增加手机字段
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)  # 增加用户头像字段, image/%Y/%m代表上传时按年月文件夹进行, default设置的是默认头像路径

    class Meta:
        verbose_name = "用户信息"  # 设置UserProfle这个类的别名
        verbose_name_plural = verbose_name  # 设置别名的复数形式

    def __str__(self):
        return self.username  # 当使用print打印时, 把继承的username字段打印出来


class EmailVerifyRecord(models.Model):  # 邮箱验证码功能
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码")), max_length=10, verbose_name="发送类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):  # 主页轮播图功能
    title = models.CharField(max_length=100, verbose_name="标题")  # 轮播图标题
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100)  # 轮播图图像地址
    url = models.URLField(max_length=200, verbose_name="访问地址")  # 轮播图的url
    index = models.IntegerField(default=100, verbose_name="显示顺序")  # 轮播图的显示顺序编号
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")  # 轮播图添加时间

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
