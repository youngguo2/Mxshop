__author__ = 'Yuxiang'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = '__all__'


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True,
                                         format='%Y-%m-%d %H:%M')  # 只get不post: read_only  只post不get: write_only

    class Meta:
        model = UserLeavingMessage
        fields = ['user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time']  # 删除需要传入id


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    展示用户收藏列表
    """
    goods = GoodsSerializer()  # 外键嵌套serializer

    class Meta:
        model = UserFav
        fields = '__all__'

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 覆写user成前端传入的当前用户

    class Meta:
        model = UserFav
        # serializer中配置unique_together
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=UserFav.objects.all(),
        #         fields=['user', 'goods'],
        #         message='已经收藏'
        #     )
        # ]

        fields =['user', 'goods', 'id']  # id用于删除记录