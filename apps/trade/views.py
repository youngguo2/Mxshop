from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissons import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer


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

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer
