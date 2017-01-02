from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect

from models import Attention
from forms import ContactForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


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


def autorisation(request):
    if request.method == 'GET':
        logout(request)
        template = loader.get_template('autorisation.html')
        context = RequestContext(request, {'form': LoginForm()})
        return HttpResponse(template.render(context))
    else:
        form = LoginForm(request.POST)
        user = authenticate(username=form['login'].value(),
                            password=form['password'].value())
        print request.POST
        print form['login'].value(), form['password'].value()
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

        if user is not None:
            context = RequestContext(request, {
                'login': user.username,
                'active': t,
            })
        else:
            context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(template.render(context))


def is_gast(request):
    return not request.user.is_authenticated()
