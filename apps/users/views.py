from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import SmsSerializer
from utils.yunpian import Yunpian
from utils.random_str import generate_code
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证,继承 ModelBackend, 套路如下
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, GenericViewSet):
    """
    creat： 发送并存储验证码
    """
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        """
        重写creat完成model的记录添加
        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)  # get_serializer指向SmsSerializer
        serializer.is_valid(raise_exception=True)   # 若异常则直接抛出400错误

        #生成验证码
        yunpian = Yunpian()
        code = generate_code()
        mobile = serializer.validated_data['mobile']
        sms_status = yunpian.send_sms(code, mobile)

        #将验证码发送状态发送到前端

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)