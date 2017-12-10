from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.conf import settings

from .models import Attention, ADFSUser
from .forms import ContactForm
from django.contrib.auth import authenticate, login

from base64 import b64decode
import base64
from django.core.files.base import ContentFile

import requests
import json

try:
    import urlparse
    from urllib import urlencode
except:
    import urllib.parse as urlparse
    from urllib.parse import urlencode


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
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

        if data.get('avatar', None):
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
            return HttpResponse(
                json.dumps({'error': 'Incorrect login or password'}),
                status=403)

        if user is not None:
            context = RequestContext(request, {
                'login': user.username,
                'active': t,
            })
        else:
            context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(json.dumps({'login': user.username, 'active': t}))


@csrf_exempt
def autorisation_vk(request):
    code = request.GET['code']
    query_string = urllib.urlencode({
        'client_id': settings.OAUTH_PUBLIC_CONFIGS['vk']['client_id'],
        'code': code,
        'client_secret': settings.OAUTH_PRIVATE_CONFIGS['vk']['client_secret'],
        'redirect_uri': settings.OAUTH_PUBLIC_CONFIGS['vk']['redirect_uri'],
    })

    r = requests.get("https://oauth.vk.com/access_token?%s" % query_string)
    params = json.loads(r.text)
    access_token = params['access_token']


@csrf_exempt
def autorisation_github(request):
    try:
        code = request.GET['code']
        client_id = settings.OAUTH_PUBLIC_CONFIGS['github']['client_id']
        client_secret = \
            settings.OAUTH_PRIVATE_CONFIGS['github']['client_secret']

        r = requests.post("https://github.com/login/oauth/access_token",
                          data={
                              'client_id': client_id,
                              'client_secret': client_secret,
                              'code': code,
                              'accept': 'application/json',
                          })

        params = urlparse.parse_qs(r.text)
        access_token = params['access_token']
        response = requests.get(
            "https://api.github.com/user/emails?access_token=%s" %
            access_token[0]).json()

        response_user = requests.get(
            "https://api.github.com/user?access_token=%s" %
            access_token[0]).json()

        emails = []
        for email in response:
            if email['verified']:
                emails.append(email['email'])

        users = ADFSUser.objects.all()
        for user in users:
            if user.email in emails:
                new_user = authenticate(username=user.username, api=True)
                login(request, new_user)
                context = RequestContext(request, {})
                template = loader.get_template('gratulations.html')
                return HttpResponse(template.render(context))

        user = ADFSUser.objects.create_user(
            username=response_user['login'],
            email=response[0]['email'],
            password='rasim')

        new_user = authenticate(username=user.username, api=True)
        login(request, new_user)
        context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(template.render(context))
    except Exception:
        return redirect('/')


def is_gast(request):
    return not request.user.is_authenticated()
