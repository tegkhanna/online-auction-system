from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from portal.models import banned_user
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone, dateparse

from datetime import datetime, timedelta
import string,random
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
        if form.is_valid():
            pass
        else:
            messages.error(request,"Enter Correct Values In All The Fields")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        new_user = form.save(commit=False)
        try:
            quer = UserDetail.objects.get(email=new_user.email)
        except UserDetail.DoesNotExist:
            try:
                quer=UserDetail.objects.get(userName=new_user.userName)
            except UserDetail.DoesNotExist:
                new_user.password=pbkdf2_sha256.encrypt(new_user.password,rounds=12000,salt_size=32)
                new_user.save()
                try:
                    send_mail("Thanks for registering with us.", "", settings.EMAIL_HOST_USER, [new_user.email],
                          fail_silently=True,html_message="<h1>THANKS ALOT FOR JOINING OUR ONLINE AUCTION SYSTEM</h1>")
                except:
                    pass
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
            if pbkdf2_sha256.verify(request.POST['password'],m.password):
                request.session['inSession'] = False
                request.session['adminSession'] = True
                return HttpResponseRedirect(reverse('portal:adminPage'))
            else:
                messages.error(request, "Wrong username or password.")
                return HttpResponseRedirect(reverse('signup:LoginForm'))
        except Admins.DoesNotExist:
            try:

                m = UserDetail.objects.get(userName=request.POST['username'])
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
        try:
            form = self.form_class
            quer = UserDetail.objects.get(pk=request.session['userID'])
            if(quer.visa_set.count()==0):
                return render(request, self.template_name, {'form':form, 'userName':quer.name, 'isReg':0})
            else:
                return render(request, self.template_name, {'form':form, 'userName':quer.name, 'isReg':1})
        except:
             return HttpResponseRedirect(reverse('signup:LoginForm'))


    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            try:
                date = dateparse.parse_date(request.POST['expDate'])
                if(date < date.today()):
                    messages.error(request,"VISA is already expired")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except ValueError:
                messages.error(request,"Enter correct date time values")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            quer.visa_set.create(visaNum = request.POST['visaNum'], expDate = request.POST['expDate'])
            messages.success(request, "Visa Registered")
            return HttpResponseRedirect(reverse('portal:index'))
        except UserDetail.DoesNotExist:
            messages.error(request, "You are not logged in.")
            return HttpResponseRedirect(reverse('signup:LoginForm'))


class PasswordRecover(generic.edit.FormView):
    form_class = PassRecoverForm
    template_name='signup/passrecover.html'
    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        if UserDetail.objects.filter(email=request.POST['email']).exists()==False:
            messages.error(request, "This Email Id is not associated with any account.")
            return HttpResponseRedirect(reverse('signup:PasswordRecover'))
        else:
            def id_generator(size=25, chars=string.ascii_uppercase + string.digits+string.ascii_lowercase):
                return ''.join(random.choice(chars) for _ in range(size))
            userid=UserDetail.objects.get(email=request.POST['email']).id
            link = id_generator()
            if PasswordRecovery.objects.filter(email=request.POST['email']).exists():
                quer=PasswordRecovery.objects.get(email=request.POST['email'])
                quer.link=link
                quer.save()
            else:
                quer=PasswordRecovery(link=link,userid=userid,email=request.POST['email'])
                quer.save()
            try:
                recoverlink="http://127.0.0.1:8000/signup/passwordchange/"+link
                uname=UserDetail.objects.get(email=request.POST['email']).userName
                message="<h3><a href="+recoverlink+">Click here to reset your password</a></h3><br><h3>If you forgot your username here it is:"+uname+"</h3>"
                send_mail("PASSWORD RESET FOR ONLINE AUCTION SYSTEM", "If you never requested for it kindly ignore.", settings.EMAIL_HOST_USER, [request.POST['email']],
                      fail_silently=False, html_message=message)
                messages.success(request,"A password recovery link has been sent to your mail.")
                return HttpResponseRedirect(reverse('signup:PasswordRecover'))
            except:
                messages.error(request, "Our mailing servers are down at the moment.Try again later.")
                return HttpResponseRedirect(reverse('signup:PasswordRecover'))


class PasswordChanger(generic.edit.FormView):
    form_class = PassChangeForm
    template_name = 'signup/passchange.html'
    def get(self, request,getlink, *args, **kwargs):
        recoverlink=getlink
        if PasswordRecovery.objects.filter(link=recoverlink).exists()==False:
            return HttpResponseRedirect(reverse('signup:index'))
        else:
            form = self.form_class
            return render(request, self.template_name, {'form': form})
    def post(self, request,getlink, *args, **kwargs):
        recoverlink =getlink
        userid=PasswordRecovery.objects.get(link=recoverlink).userid
        if UserDetail.objects.filter(id=userid).exists():
            quer= UserDetail.objects.get(id=userid)
            quer.password=pbkdf2_sha256.encrypt(request.POST["password"],rounds=12000,salt_size=32)
            quer.save()
            user=PasswordRecovery.objects.get(link=recoverlink)
            user.delete()
            messages.success(request,"Password reset successful.")
            return HttpResponseRedirect(reverse('signup:LoginForm'))
        else:
            messages.success(request, "You have already reset your password.")
            return HttpResponseRedirect(reverse('signup:index'))











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