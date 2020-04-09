__author__ = 'Yuxiang'

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    信号量post_save方法，响应sender保存后的操作。created若建立则置为True,instance为保存的实例。在APPS中还要设置函数
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        # Token.objects.create(user=instance) JWT不需要token
        password = instance.password
        instance.set_password(password)
        instance.save()