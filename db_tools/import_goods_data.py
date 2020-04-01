import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django
django.setup()

from goods.models import Goods, GoodsImage, GoodsCategory
from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()

    category_name = goods_detail['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        # goods.category = category 有两个queryset 报错。取【0】
        #ValueError: Cannot assign "<QuerySet [<GoodsCategory: 根茎类>, <GoodsCategory: 根茎类>]>": "Goods.category" must be a "GoodsCategory" instance.
        goods.category = category[0]
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""
    goods.save()

    for good_image in goods_detail['images']:
        goodsimage_instance = GoodsImage()
        goodsimage_instance.goods = goods
        goodsimage_instance.image = good_image
        goodsimage_instance.save()