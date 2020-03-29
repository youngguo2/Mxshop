from django.db import models
from datetime import datetime

from users.models import BaseModel


class GoodsCategory(BaseModel):
    '''
    商品类别 用一个MODEL实现多级目录
    '''
    CATEGORY_TYPE = (
        (1, '一级目录'),
        (2, '二级目录'),
        (3, '三级目录'),
    )

    name = models.CharField(max_length=20, verbose_name='类别名', default='', help_text='类别描述')
    code = models.CharField(max_length=20, verbose_name='类别code', default='', help_text='类别代码')
    desc = models.TextField(verbose_name='类别描述', default='', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类别级别', help_text='类别级别')
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类目级别', \
                                        help_text='父类别级别', related_name='sub_cat')      # foreignkey指向自己用’self'
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
