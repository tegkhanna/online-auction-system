from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from portal.models import banned_user
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
# Create your views here.
from .models import *
from .forms import *
# Create your views here.
class Signup(generic.edit.FormView):
    form_class  = UserForm
    template_name = 'signup/SignUpForm.html'
    def get(self, request, *args, **kwargs):
        try:
            form = self.form_class
            if(((request.session['inSession'] is False) or (request.session['inSession'] is None)) and ((request.session['adminSession'] is False))):
                return render(request, self.template_name, {'form':form})
            elif((request.session['adminSession'] is True)):
                return HttpResponseRedirect(reverse('portal:adminPage'))
            else:
                return HttpResponseRedirect(reverse('portal:index'))
        except KeyError:
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        new_user = form.save(commit=False)
        try:
            quer = UserDetail.objects.get(email=new_user.email)
        except UserDetail.DoesNotExist:
            try:
                quer=UserDetail.objects.get(userName=new_user.userName)
            except UserDetail.DoesNotExist:
                new_user.password=pbkdf2_sha256.encrypt(new_user.password,rounds=12000,salt_size=32)
                new_user.save()
                quer=UserDetail.objects.get(userName=new_user.userName)
                request.session['userID'] = quer.id
                request.session['inSession'] = True
                messages.success(request,"Successfully registered.Thanks for joining.")
                return HttpResponseRedirect(reverse('portal:index'))
            else:
                messages.error(request, "The username or email already exists.")
                return HttpResponseRedirect(reverse('signup:signUpPage'))
        else:
            messages.error(request, "The username or email already exists.")
            return HttpResponseRedirect(reverse('signup:signUpPage'))



class IndexView(generic.TemplateView):
    template_name = 'signup/index.html'
    def get(self, request, *args, **kwargs):
        if('inSession' in request.session and 'adminSession' in request.session):
            if  (((request.session['inSession'] is False) or (request.session['inSession'] is None)) and ((request.session['adminSession'] is False))):
                return render(request, self.template_name)
            elif((request.session['adminSession'] is True)):
                return HttpResponseRedirect(reverse('portal:adminPage'))
            else:
                return HttpResponseRedirect(reverse('portal:index'))
        else:
            return render(request, self.template_name)



class LoginForm(generic.edit.FormView):
    form_class = LoginForm
    template_name = 'signup/loginForm.html'
    def get(self, request, *args, **kwargs):
        try:
            form = self.form_class
            if(((request.session['inSession'] is False) or (request.session['inSession'] is None)) and ((request.session['adminSession'] is False))):
                return render(request, self.template_name, {'form':form})
            elif((request.session['adminSession'] is True)):
                return HttpResponseRedirect(reverse('portal:adminPage'))
            else:
                return HttpResponseRedirect(reverse('portal:index'))
        except KeyError:
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            m = Admins.objects.get(userName=request.POST['username'])
            if (request.POST['password'] == m.password):
                request.session['inSession'] = False
                request.session['adminSession'] = True
                return HttpResponseRedirect(reverse('portal:adminPage'))
            else:
                messages.error(request, "Wrong username or password.")
                return HttpResponseRedirect(reverse('signup:LoginForm'))
        except Admins.DoesNotExist:
            try:

                m = UserDetail.objects.get(userName=request.POST['username'])
                print(m.password)
                if banned_user.objects.filter(userid=m.id).exists():
                    messages.error(request, "Your account is banned.")
                    return HttpResponseRedirect(reverse('signup:LoginForm'))

                elif pbkdf2_sha256.verify(request.POST['password'],m.password):
                    request.session['userID'] = m.id
                    request.session['inSession'] = True
                    request.session['adminSession'] = False
                    messages.success(request, "WELCOME")
                    return HttpResponseRedirect(reverse('portal:index'))
                else:
                    messages.error(request, "Wrong username or password.")
                    return HttpResponseRedirect(reverse('signup:LoginForm'))
            except UserDetail.DoesNotExist:
                messages.error(request, "Wrong username or password.")
                return HttpResponseRedirect(reverse('signup:LoginForm'))

class VisaForm(generic.edit.FormView):
    form_class  = VisaForm
    template_name = 'signup/visa.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        quer = UserDetail.objects.get(pk=request.session['userID'])
        if(quer.visa_set.count()==0):
            return render(request, self.template_name, {'form':form, 'userName':quer.name, 'isReg':0})
        else:
            return render(request, self.template_name, {'form':form, 'userName':quer.name, 'isReg':1})

    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            quer.visa_set.create(visaNum = request.POST['visaNum'], expDate = request.POST['expDate'])
            messages.success(request, "Visa registered")
            return HttpResponseRedirect(reverse('portal:index'))
        except UserDetail.DoesNotExist:
            messages.error(request, "You are not logged in.")
            return HttpResponseRedirect(reverse('signup:LoginForm'))
def Logout(request):
    try:
        request.session['userID']=None
        request.session['inSession'] = False
        request.session['adminSession'] = False

        if 'adminSession' in request.session:
            if request.session['adminSession'] == True or request.session['adminSession'] == None:
                request.session['adminSession'] = False
        
    except KeyError:
        pass
    messages.success(request, "You have successfully logged out.")
    return HttpResponseRedirect(reverse('signup:LoginForm'))