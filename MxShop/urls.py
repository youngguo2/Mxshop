"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from MxShop.settings import MEDIA_ROOT  # 以上两步导入media路径所需模块
#生成可视化文档的url设置
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
import xadmin

# from goods.views_base import GoodsListView
from goods.views import GoodsListViewset, CategoryViewSet, GoodsPriceRangeViewSet

router = DefaultRouter()
# 配置goods的url,自动将'get'和'list'绑定
router.register('goods', GoodsListViewset, basename='goods')    #注意不要加/，系统默认会加上
# 配置CategoryViewSet的url
router.register('categorys', CategoryViewSet, basename='categorys')
# 配置GoodsPriceRangeViewSet的url
router.register('priceRange', GoodsPriceRangeViewSet, basename='priceRange')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 配置上传文件的访问URL。 serve中有path和document_root两个参数
    # path('goods/', GoodsListView.as_view(), name='goods-list'),
    path('', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'docs/', include_docs_urls(title='慕学生鲜')),  #生成文档操作
]
