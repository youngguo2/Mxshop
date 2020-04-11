from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods
from users.models import BaseModel
User = get_user_model()


class UserFav(BaseModel):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品id", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'goods']  # 联合索引，避免生成两条user goods同时重复的记录

    def __str__(self):
        return self.user.username


class UserLeavingMessage(BaseModel):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                      help_text="留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default="", verbose_name="主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件", help_text="上传的文件")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(BaseModel):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default="", verbose_name="省份")
    city = models.CharField(max_length=100, default="", verbose_name="城市")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
