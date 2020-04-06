__author__ = 'Yuxiang'

import re
import datetime

from rest_framework import serializers

from .models import VerifyCode


class SmsSerializer(serializers.Serializer):
    """
    验证手机号码
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 验证手机是否已注册
        if VerifyCode.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        # 验证手机号是否合法
        key = "^(13[0-9]|14[5-9]|15[0-3,5-9]|16[2,5,6,7]|17[0-8]|18[0-9]|19[0-3,5-9])\\d{8}$"
        if not re.match(key, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证验证码发送频率
        a_minute_age = datetime.datetime.now()- datetime.timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=a_minute_age).count():
            raise serializers.ValidationError('距离上次发送未超过60s')

        return mobile