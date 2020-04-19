from datetime import datetime

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from utils.permissons import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect

from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from MxShop.settings import private_key_path, ali_pub_key_path


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # queryset = ShoppingCart.objects.filter()
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.goods_num -= instance.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.filter(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer


class OrderViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    订单管理
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # 取购物车中的物品加入订单
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = cart.goods
            order_goods.nums = cart.nums
            order_goods.order = order
            order_goods.save()
        # 删除购物车
            cart.delete()
        return order


class AlipayView(APIView):
    def get(self, request):
        """
        处理支付宝return url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016102300747529",
            app_notify_url="http://140.143.127.148/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://140.143.127.148:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)  # filter返回一个数组
            # 修改售卖数
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()  # 外键不需要objects.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()
            # 修改订单状态
            existed_order.pay_status = trade_status
            existed_order.trade_no = trade_no
            existed_order.pay_time = datetime.now()
            existed_order.save()

            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)  # 进入个人订单页面
        else:
            response = redirect('index')
        return response

    def post(self, request):
        """
        处理支付宝notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016102300747529",
            app_notify_url="http://140.143.127.148/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://140.143.127.148:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)  # filter返回一个数组
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response('success')