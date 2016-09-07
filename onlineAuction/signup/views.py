from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
from .models import *
from .forms import *
# Create your views here.
class FormView(generic.edit.FormView):
	form_class  = UserForm
	template_name = 'signup/SignUpForm.html'

class LoginForm(generic.edit.FormView):
    form_class = LoginForm
    template_name = 'signup/loginForm.html'

class VisaForm(generic.edit.FormView):
    form_class  = VisaForm
    template_name = 'signup/visa.html'


def signup(request):
    form = UserForm(request.POST)
    new_user = form.save(commit=False)

    try:
    	quer = UserDetail.objects.get(email=new_user.email)
    except UserDetail.DoesNotExist:
        try:
            quer=UserDetail.objects.get(userName=new_user.userName)
        except UserDetail.DoesNotExist:
            new_user.save()
            return HttpResponseRedirect(reverse('signup:LoginForm'))
        else:
            return HttpResponse("Your username or email exist.")
    else:
       return HttpResponse("Your username or email exist.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
   # return HttpResponseRedirect(reverse('polls:index'))

def login(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = UserDetail.objects.get(userName=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['userID'] = m.id
            return HttpResponse("you are logged in.")
    except UserDetail.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")


def visaReg(request):
    try:
        quer = UserDetail.objects.get(pk=request.session['userID'])
        if(quer.visa_set.count()==0):
            quer.visa_set.create(visaNum = request.POST['visaNum'], expDate = request.POST['expDate'])
            HttpResponse("Visa Registered.")
        else:
            HttpResponse("already registered.")
    except UserDetail.DoesNotExist:
        HttpResponse("you are not login.")