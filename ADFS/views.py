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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():
        if True:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            a = Attention.objects.all().create(name=form['name'].value(),
                                               vkLink=form['vkLink'].value(),
                                               phone=form['phone'].value(),
                                               team=form['team'].value(),
                                               first_league=form['first_league'].value(),
                                               pokal=form['pokal'].value(),
                                               winter_pokal=form['winter_pokal'].value())

            return HttpResponseRedirect('/attention/%i' % a.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'attention.html', {'form': form})


def autorisation(request):
    if request.method == 'GET':
        logout(request)
        template = loader.get_template('autorisation.html')
        context = RequestContext(request, {'form' : LoginForm()})
        return HttpResponse(template.render(context))
    else:
        form = LoginForm(request.POST)
        user = authenticate(username=form['login'].value(), password=form['password'].value())
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
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

        if user is not None:
            context = RequestContext(request, {
                'login' : user.username,
                'active' : t,
            })
        else:
            context = RequestContext(request, {})
        template = loader.get_template('gratulations.html')
        return HttpResponse(template.render(context))


def is_gast(request):
    return not request.user.is_authenticated()
