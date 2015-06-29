from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Element
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'Elements': Element.objects.order_by('description'),
    })
    return HttpResponse(template.render(context))
