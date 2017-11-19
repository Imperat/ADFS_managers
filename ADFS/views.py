from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Attention, ADFSUser
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout

from base64 import b64decode
import base64
from django.core.files.base import ContentFile

import json
# Create your views here.

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)

def survey(request):
    template = loader.get_template('base_react.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def regl(request):
    template = loader.get_template('reglam.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def attentions(request):
    template = loader.get_template('attention_view.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def view_attention(request, id):
    template = loader.get_template('attention_view.html')
    context = RequestContext(request, {
        'attention': get_object_or_404(Attention, pk=id)
    })
    return HttpResponse(template.render(context))


def reglament(request):
    template = loader.get_template('reglament.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def register_attention(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            a = Attention.objects.all().create(
                name=form['name'].value(),
                vkLink=form['vkLink'].value(),
                phone=form['phone'].value(),
                team=form['team'].value(),
                first_league=form['first_league'].value(),
                pokal=form['pokal'].value(),
                winter_pokal=form['winter_pokal'].value())

            return HttpResponseRedirect('/attention/%i' % a.id)
    return render(request, 'attention.html', {'form': form})

@csrf_exempt
def register(request):
    data = request.POST.dict()

    # print (data)

    try:
        user = ADFSUser.objects.create_user(
          username=data['login'],
          email=data['email'],
          password=data['password'])

        if data.get('avatar', None) != None:
            user.avatar = ContentFile(b64decode(data['avatar']), 'rosimka.png')

        user.save()
    except Exception as e:
        print(e)
        return HttpResponse('{"error": "%s"}' % e.message,
                            content_type='application/json',
                            status=400)
    else:
        return HttpResponse('{"info": "User created"}',
                            content_type='application/json',
                            status=201)

@csrf_exempt
def autorisation(request):
    if request.method == 'GET':
        context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(template.render(context))
    else:
        user = authenticate(username=request.POST['login'],
                            password=request.POST['password'])

        t = False
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(request, user)
                t = True
            else:
                print("The password is valid, but the account is disabled!")
        else:
            print("The username and password were incorrect.")
            return HttpResponse(json.dumps({ 'error': 'Incorrect login or password' }), status=403)

        if user is not None:
            context = RequestContext(request, {
                'login': user.username,
                'active': t,
            })
        else:
            context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(json.dumps({ 'login': user.username, 'active': t }))


def is_gast(request):
    return not request.user.is_authenticated()
