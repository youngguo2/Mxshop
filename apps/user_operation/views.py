from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, UserAddressSerializer
from utils.permissons import IsOwnerOrReadOnly


class AddressViewset(viewsets.ModelViewSet):
    """
    ModelViewset 相当于把增删改查mixin打包
    用户地址
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    serializer_class = UserAddressSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        我的留言列表
    create:
        创建留言
    destroy:
        删除留言
    """
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)
    serializer_class = LeavingMessageSerializer


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    list:
        获取用户收藏列表
    create:
        收藏
    destroy:
        取消收藏
    retrieve:
        判断某商品是否已经收藏
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        return UserFavSerializer
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]  # 登陆验证放在局部做
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'goods_id'  # 配合retrievemodelMixin使用。查询返回的字段名，默认为pk

    # class中所有操作都是对user各自的记录进行的
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)