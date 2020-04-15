__author__ = 'Yuxiang'

import time
from random import Random

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer


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
