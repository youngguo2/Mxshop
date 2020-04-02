from django.views.generic.base import View
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

from goods.models import Goods

class GoodsListView(View):

    def get(self, request):
        goods = Goods.objects.all()[:10]
        # 使用serializers.serialize方法对于queryset进行json.dumps的序列化转化
        json_data = serializers.serialize('json', goods)

        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(json.loads(json_data), safe=False)