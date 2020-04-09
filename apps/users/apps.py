from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户管理'

    def ready(self):
        """
        信号量设置
        :return:
        """
        import users.signals