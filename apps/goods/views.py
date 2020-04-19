from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination  #分页
from rest_framework import mixins, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend   # 复杂过滤功能用的是django-filter
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin  # 内存中设置缓存,重启后消失
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexCategorySerializer
from goods.filters import GoodsFilter


# class GoodsListView(APIView):
#     """
#     备注：会显示在api doc中,商品列表页
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True) #many 用于goods为queryset时
#         return Response(goods_serializer.data)

# class GoodsListView(generics.ListAPIView):
#     """
#     利用genetics简化以上代码
#     商品列表页
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination  # 分页

class GoodsPagination(PageNumberPagination):
    """
    定制化分页
    """
    page_size = 10
    page_size_query_param = 'page_size'  # url中定制化的查询变量,可动态设置page_size=100
    page_query_param = 'page'  # url中定制化的查询变量,可动态设置page=2
    max_page_size = 100


# class GoodsPriceRangeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     list: 价格分区数据
#     """


class GoodsListViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    利用Viewsets进一步优化，与urls中的Router配合
    商品列表页
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  # 用户限速通过用户ID，匿名用户（未登录）限速通过IP地址
    queryset = Goods.objects.all()  # 属性
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  # 分页

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # authentication_classes = (TokenAuthentication, )  # 设置局部认证，列表页不需要登陆后访问，所以需注释掉
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤，搜索，排序
    # filterset_fields = ['name', 'shop_price'] # drf中的过滤功能

    #利用django-filter中的过滤功能，filterset_class实现复杂功能过滤
    filterset_class = GoodsFilter

    #利用drf 的filters 实现搜索和排序
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']

    # 最简易过滤方法
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min', 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset


# RetrieveModelMixin用于获得详情页面，自动注册<int:id>这种的url并自动返回id对应的页面
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        实现商品分类数据的嵌套显示
        此处为定义可视化界面的action的备注
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示轮播图
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        展示类别商品
    """
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer


