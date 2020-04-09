__author__ = 'Yuxiang'

import re
import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode
User = get_user_model()

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


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册验证
    """
    code = serializers.CharField(max_length=4, min_length=4, error_messages = {
                                                       'required': '请输入验证码',
                                                       'max_length': '验证码格式错误',
                                                       'min_length': '验证码格式错误',
                                                   }, help_text='验证码', label='验证码', write_only=True)
    # write_only：不参与序列化后return，用于field中部返回的字段
    # 利用validators类验证用户名是否已注册, 注意validators是列表
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用戶已存在')])

    password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True)

    def validate_code(self, code):
        """
        验证验证码是否正确
        :param code:
        :return:
        """
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username'])  # 前端传来的数据都在self.initial_data中
        if verify_records:
            last_record = verify_records.order_by('-add_time')[0]
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        将验证后的结果整理返回存入Model
        :param attrs:
        :return:
        """
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'code', 'mobile', 'password']