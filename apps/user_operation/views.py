from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissons import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]  # 登陆验证放在局部做
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'goods_id'  # 配合retrievemodelMixin使用。查询返回的字段名，默认为pk

    # class中所有操作都是对user各自的记录进行的
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)