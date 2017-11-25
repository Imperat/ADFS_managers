from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader

from carusele.models import Element, News


def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'Elements': Element.objects.order_by('description'),
    })
    return HttpResponse(template.render(context))


def article(request, id):
    template = loader.get_template('article.html')
    poll = get_object_or_404(News, pk=id)
    context = RequestContext(request, {
        'article': poll,
        'number': id,
    })
    return HttpResponse(template.render(context))

def articles(request):
    template = loader.get_template('articles.html')
    articles = News.objects.order_by('-pubdate').all()
    context = RequestContext(request, {
        'articles': articles,
    })

    return HttpResponse(template.render(context))
