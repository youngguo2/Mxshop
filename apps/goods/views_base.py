from django.views.generic.base import View
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
import json

from goods.models import Goods

class GoodsListView(View):

    def get(self, request):
        json_data = []
        goods = Goods.objects.all()[:10]
        for good in goods:
            json_data.append(model_to_dict(good))

        return HttpResponse(json.dumps(json_data), content_type='application/json')