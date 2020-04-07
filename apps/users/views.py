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
from users.models import VerifyCode
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

        mobile = serializer.validated_data['mobile']

        #生成并发送验证码
        yunpian = Yunpian()
        code = generate_code()
        sms_status = yunpian.send_sms(code, mobile)

        #将验证码发送状态发送到前端,若成功则保存到数据库
        if sms_status['code'] != 0:
            return Response({
                mobile: sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode.objects.create(mobile=mobile, code=code)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)
