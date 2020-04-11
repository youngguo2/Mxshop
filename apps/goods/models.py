from django.db import models
from datetime import datetime

from users.models import BaseModel

from DjangoUeditor.models import UEditorField

class GoodsCategory(BaseModel):
    """
    商品类别 用一个MODEL实现多级目录
    """
    CATEGORY_TYPE = (
        (1, '一级目录'),
        (2, '二级目录'),
        (3, '三级目录'),
    )
    # help_text 在xadmin后台的栏目下方显示，给用户一个描述，同时可以在文档中作为description展示
    name = models.CharField(max_length=20, verbose_name='类别名', default='', help_text='类别描述')
    code = models.CharField(max_length=20, verbose_name='类别code', default='', help_text='类别代码')
    desc = models.TextField(verbose_name='类别描述', default='', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='类别级别', help_text='类别级别')
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类目级别', \
                                        help_text='父类别级别', related_name='sub_cat', on_delete=models.CASCADE)      # foreignkey指向自己用’self'
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(BaseModel):
    """
    商品分类处展示商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, related_name='brands', verbose_name='商品类目')
    name = models.CharField(max_length=20, verbose_name='品牌名', help_text='品牌名')
    image = models.ImageField(upload_to='brand/', max_length=200, verbose_name='品牌logo', help_text='品牌logo')
    desc = models.TextField(max_length=200, default='', verbose_name='品牌描述', help_text='品牌描述')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类目", on_delete=models.CASCADE)
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    #利用UEditor编辑富文本，上传图片及文件
    goods_desc = UEditorField(verbose_name='内容', imagePath='goods/images/', width=1000, height=300, filePath='goods/files', default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_front_image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """
    每个商品的轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
