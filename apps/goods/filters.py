__author__ = 'Yuxiang'

from django.db.models import Q

import django_filters as df
from .models import Goods


class GoodsFilter(df.rest_framework.FilterSet):
    """
    商品过滤类
    """
    minprice = df.rest_framework.NumberFilter(field_name="shop_price", lookup_expr='gte')
    maxprice = df.rest_framework.NumberFilter(field_name="shop_price", lookup_expr='lte')
    # name = df.rest_framework.CharFilter(field_name='name', lookup_expr='icontains')
    top_category = df.rest_framework.NumberFilter(method='top_category_filter')  # 利用method定义过滤Model字段中没有的过滤项

    def top_category_filter(self, queryset, name, value):
        """
        功能：列出第一类的所有数据
        3个默认传递进来的参数
        :param queryset:全部52个商品实例
        :param name:top_category
        :param value:300
        :return:
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |\
                         Q(category__parent_category__parent_category_id=value))  # __指向外键对象

    class Meta:
        model = Goods
        fields = ['minprice', 'maxprice', 'top_category']
