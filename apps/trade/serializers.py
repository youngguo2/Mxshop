__author__ = 'Yuxiang'

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer


class ShoppingCartDetailSerializer(serializers, serializers.ModelSerializer):
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