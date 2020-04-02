from django.shortcuts import render
from goods.models import Goods
from goods.serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class GoodsListView(APIView):
    """
    备注：会显示在api doc中
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True) #many 用于goods为queryset时
        return Response(goods_serializer.data)