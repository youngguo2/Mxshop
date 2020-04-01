# -*- coding: utf-8 -*-
__author__ = 'bobby'

#独立使用django的model
import sys
import os

"""
__file__：当前文件路径（不在sys.path里则返回绝对路径，否则返回相对路径）
os.path.realpath(__file__): 一般返回绝对路径
os.path.dirname(os.path.realpath(__file__):去掉路径的文件名，返回目录。即pwd
pwd = 'G:\\PyProject\\MxShop\\db_tools'
sys.path.append(pwd+'../'):把文件所在根目录加入系统路径。动态获得pwd避免项目路径变化后混乱。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")：要想单独使用django的model，必须指定一个环境变量，会去settings配置找
"""
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django
django.setup()

from goods.models import GoodsCategory

from db_tools.data.category_data import row_data

# 一级类
for lev1_cat in row_data:
    lev1_intance = GoodsCategory()
    lev1_intance.code = lev1_cat["code"]
    lev1_intance.name = lev1_cat["name"]
    lev1_intance.category_type = 1
    lev1_intance.save()

#二级类
    for lev2_cat in lev1_cat['sub_categorys']:
        lev2_intance = GoodsCategory()
        lev2_intance.code = lev2_cat['code']
        lev2_intance.name = lev2_cat['name']
        lev2_intance.category_type = 2
        lev2_intance.parent_category = lev1_intance
        lev2_intance.save()

#三级类
        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_intance = GoodsCategory()
            lev3_intance.code = lev3_cat["code"]
            lev3_intance.name = lev3_cat["name"]
            lev3_intance.category_type = 3
            lev3_intance.parent_category = lev2_intance
            lev3_intance.save()

