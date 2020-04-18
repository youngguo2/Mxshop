__author__ = 'Yuxiang'

import time
from random import Random

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_pub_key_path


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = 'fields'


class ShoppingCartSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={'required': '请选择购买数量',
                                                                                'min_value': '数量不能小于1'}, label='商品数量')
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)  # serializer中的外键

    def create(self, validated_data):
        user = self.context['request'].user  # serializer中获取request user
        nums = self.validated_data['nums']
        goods = self.validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """
    订单
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField()  # 对应一个方法

    def get_alipay_url(self, obj):
        # obj指Serializer实例
        alipay = AliPay(
            appid="2016102300747529",
            app_notify_url="http://140.143.127.148/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://140.143.127.148:8000/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            # return_url="http://140.143.127.148:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        # 当前时间+ID+2位随机数
        random_ins = Random()
        return '{}{}{}'.format(time.strftime('%Y%m%d%h%m'), self.context['request'].user.id, random_ins.randint(10, 99))

    def validate(self, attrs):
        attrs['oder_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField()  # 对应一个方法

    def get_alipay_url(self, obj):
        # obj指Serializer实例
        alipay = AliPay(
            appid="2016102300747529",
            app_notify_url="http://140.143.127.148/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://140.143.127.148:8000/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
            # return_url="http://140.143.127.148:8000/alipay/return/"
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'
