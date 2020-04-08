from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    # model 都有add_time属性。建立basemodel来继承

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True # 此类不可生成对象，只能被继承使用, 用作编译时对象


class UserProfile(AbstractUser):
    '''
    用户信息
    编写OK后需到SETTING中替换掉系统用户
    '''
    name = models.CharField(max_length=30, verbose_name='姓名', default='')
    birthday = models.DateTimeField(verbose_name='出生年月', null=True, blank=True, default=None)
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), verbose_name='性别')
    email = models.CharField(max_length=40, verbose_name='邮箱', default='')
    mobile = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(BaseModel):
    '''
    手机验证码
    '''
    code = models.CharField(max_length=6, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')

    class Meta:
        verbose_name_plural = verbose_name = '手机验证码'

    def __str__(self):
        return self.code