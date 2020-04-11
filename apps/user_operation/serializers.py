__author__ = 'Yuxiang'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav


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