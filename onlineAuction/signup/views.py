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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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


class LoginForm(generic.edit.FormView):
    form_class = LoginForm
    template_name = 'signup/loginForm.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        if((request.session['inSession'] is False) or (request.session['inSession'] is None)):
            return render(request, self.template_name, {'form':form})
        else:
            return HttpResponseRedirect(reverse('portal:index'))
    def post(self, request, *args, **kwargs):
        try:
            m = UserDetail.objects.get(userName=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['userID'] = m.id
                request.session['inSession'] = True
                return HttpResponseRedirect(reverse('portal:index'))
            else:
                return HttpResponse("wronggg.")
        except UserDetail.DoesNotExist:
            return HttpResponse("Your username and password didn't match.")

class VisaForm(generic.edit.FormView):
    form_class  = VisaForm
    template_name = 'signup/visa.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        quer = UserDetail.objects.get(pk=request.session['userID'])
        if(quer.visa_set.count()==0):
            return render(request, self.template_name, {'form':form})
        else:
            return HttpResponse("already registered.")

    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            quer.visa_set.create(visaNum = request.POST['visaNum'], expDate = request.POST['expDate'])
            return HttpResponse("Visa Registered.")
        except UserDetail.DoesNotExist:
            return HttpResponse("you are not login.")

def Logout(request):
    try:
        request.session['inSession'] = False
        del request.session['userID']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('signup:LoginForm'))