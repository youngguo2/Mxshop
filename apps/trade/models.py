from django.db import models
from django.contrib.auth import get_user_model

from users.models import BaseModel
from goods.models import Goods
# get_user_model 调用setting里的USER_AUTH_MODEL
User = get_user_model()


class ShoppingCart(BaseModel):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name="购买数量")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ('%s(%d)' %(self.goods.name, self.nums))


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    #order_sn 应设置unique=True
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    #trade_no 用于支付
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)