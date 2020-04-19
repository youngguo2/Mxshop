"""
类似forms表单验证
"""
from rest_framework import serializers
from django.db.models import Q

from .models import Goods, GoodsCategory,GoodsImage, Banner, GoodsCategoryBrand, IndexAd


class GoodsImageSerializer(serializers.ModelSerializer):
    """
    序列化商品详情页的图片
    """
    class Meta:
        model = GoodsImage
        fields = ['image']


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
    sub_cat = GoodsCategorySerializer3(many=True)  # 相当于Serializer3中加入 parent_category=GoodsCategorySerializer2()

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
    category = GoodsCategorySerializer()  # 覆写modelform, 用外键的model替换外键。注意，后缀是Serializer
    images = GoodsImageSerializer(many=True)  # many=True 一对多关系。将images配置到商品的serializers里

    class Meta:
        model = Goods
        fields = '__all__'  # field完全copy Goods


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    sub_cat = GoodsCategorySerializer2(many=True)
    goods = serializers.SerializerMethodField()  # 套路如下
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        goods_json = {}
        if ad_goods:
            goods_ins = ad_goods[0].goods
            # serializer中嵌套serializer不会在资源前自动加上域名，要配置上下文
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request':self.context['request']}).data
            # goods_json.pop('category')
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) |\
                     Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods,many=True, context={'request':self.context['request']})
        return goods_serializer.data

    class Meta:
        model= GoodsCategory
        fields = '__all__'

