from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
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

        # 生成并发送验证码
        yunpian = Yunpian()
        code = generate_code()
        sms_status = yunpian.send_sms(code, mobile)

        # 将验证码发送状态发送到前端,若成功则保存到数据库
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


class UserViewset(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]

    # 覆写针对不同方法选择不同的serializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'creat':
            return UserRegSerializer
        else:
            return UserDetailSerializer

    # 覆写针对不同方法选择不同的permission
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]  # 必须加（）实例化
        elif self.action == 'creat':
            return []

        return []

    # 重写creat方法加入token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 覆写获取具体实例的方法，确保个人中心返回的数据属于当前用户
    def get_object(self):
        return self.request.user
