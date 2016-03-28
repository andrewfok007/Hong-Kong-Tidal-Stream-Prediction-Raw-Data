import json

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import loader
from datetime import datetime, timedelta
from django.forms.models import model_to_dict

from hydro.models import Hydro
from hydro.settings import headers
from django.http import JsonResponse
from django.core import serializers


def hydro_view(request):
    """
    view returns hydro main page
    """
    return render_to_response('hydro/hydro_list.html')


def hydro_JSON_data_update(request):
    """
    json data response for get request, the data delivery is capped at 15mins
    intervals
    """
    start = request.GET.get('start', "")
    end = request.GET.get('end', "")
    mode = request.GET.get('mode', "")

    if start and end and mode:
        start = datetime.strptime(start, "%d-%m-%Y %H:%M:00")
        end = start + timedelta(minutes=14.9)
        data = Hydro.objects.filter(
            mode=mode, date__range=[start, end]).order_by("date")
    else:
        data = []
    data = serializers.serialize('json', data)
    data = [dict(d["fields"]) for d in json.loads(data)]
    return HttpResponse(json.dumps(data), content_type='application/json')
