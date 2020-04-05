"""
类似forms表单验证
"""
from rest_framework import serializers

from .models import Goods, GoodsCategory


class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    序列化商品三级种类
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    序列化商品二级种类
    """
    # 这种写法无效：parent_category_set = GoodsCategorySerializer3(many=True)
    sub_cat = GoodsCategorySerializer3(many=True) #相当于Serializer3中加入 parent_category=GoodsCategorySerializer2()

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    序列化商品一级种类
    """
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    """
    序列化商品
    """
    category = GoodsCategorySerializer()  #覆写modelform, 用外键的model替换外键。注意，后缀是Serializer

    class Meta:
        model = Goods
        fields = '__all__'  #field完全copy Goods