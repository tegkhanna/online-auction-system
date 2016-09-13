from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.
from datetime import datetime, timedelta
from signup.models import UserDetail
from portal.models import articlereg

from portal.models import banned_user
def isadmin(request):
    if 'adminSession' in request.session:
        if request.session['adminSession']==True:
                return True
        else:
            return False
    else:
        return False

def adminPage(request):
    if isadmin(request):
	    context = {'details': UserDetail.objects.all()}
	    template_name='portal/adminPage.html'
	    return render(request, template_name, context)
    else:
        return HttpResponse("Login as admin to proceed.")




def deleteUser(request,id):
    if isadmin(request):
	    b = UserDetail.objects.get(pk=id)
	    b.delete()
	    return HttpResponseRedirect(reverse('portal:adminPage'))
    else:
        return HttpResponse("Login as admin to proceed.")

def banUser(request,id):
    if isadmin(request):
	    if banned_user.objects.filter(userid=id).exists():
		    pass
	    else:
		    ob=banned_user(userid=id)
		    ob.save()
	    return HttpResponseRedirect(reverse('portal:adminPage'))
    else:
        return HttpResponse("Login as admin to proceed.")
def showArticleDetails(request,id):
    if isadmin(request):
        context = {'details': articlereg.objects.filter(userid=id)}
        template_name = 'portal/adminPageShowArticles.html'
        return render(request, template_name, context)
    else:
        return HttpResponse("Login as admin to proceed.")

def deleteArticle(request,userid,id):
    if isadmin(request):
	    b = articlereg.objects.get(pk=id)
	    b.delete()
	    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Login as admin to proceed.")






from .forms import *
class IndexView(generic.TemplateView):
    template_name = 'portal/index.html'
    
    def get(self, request, *args, **kwargs):
        try:
            context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
            return render(request, self.template_name, context)
        except KeyError:
            return HttpResponseRedirect(reverse("signup:LoginForm"))

   


class RegForm(generic.edit.FormView):
    form_class  = RegForm
    template_name = 'portal/articleForm.html'
    def get(self, request, *args, **kwargs):
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name, 'form':self.form_class}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
           # time = clean(request.POST['timestart'])
           # now = datetime.now()
           # deltaNow = timedelta(days = int(now.day),hours = int(now.hour),minutes = int(now.minute),seconds = int(now.second))
           # delta = timedelta(days = int(time.day),hours = int(time.hour),minutes = int(time.minute),seconds = int(time.second))
          #  timedif = (deltaNow - delta).seconds
          #  stat = None
           # if(time < datetime.datetime.now()):
           #     stat = "sold"
           # elif(timedif > 3600):
            #    stat = "inactive"
            #elif(timedif < 3600 and timedif > 0):
            #    stat = "active"
            art=quer.articlereg_set.create( status = "active",
                                        timestart=request.POST['timestart'],articlename=request.POST['articlename'],
                                        category=request.POST['category'],desc=request.POST['desc'],
                                        minbid=request.POST['minbid'])
            art.articleimage_set.create(image=request.FILES['image'])
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            return HttpResponse("Article NOT Registered.")

class EditArticle(generic.edit.FormView):
    form_class  = EditRegForm
    template_name = 'portal/articleForm.html'
    def get(self, request,a_id, *args, **kwargs):
        data = articlereg.objects.get(pk=int(a_id))
        form = self.form_class(initial = {'status' : data.status, 
                                        'timestart':data.timestart,
                                        'articlename':data.articlename,
                                        'category':data.category,
                                        'desc':data.desc,
                                        'minbid':data.minbid,
                                        })

        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name,
                     'form':form}
        return render(request, self.template_name, context)
    def post(self, request,a_id, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            art = quer.articlereg_set.get(pk=int(a_id))
            art.status = request.POST['status']
            art.timestart=request.POST['timestart']
            art.articlename=request.POST['articlename']
            art.category=request.POST['category']
            art.desc=request.POST['desc'],
            art.minbid=request.POST['minbid']
            img = art.articleimage_set.reverse()[0]
            img.image =request.FILES['image']
            img.save()
            art.save()
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            return HttpResponse("Article NOT Registered.")


class UserShowArticles(generic.TemplateView):
    template_name = 'portal/usershowarticle.html'
    def get(self, request, *args, **kwargs):
        quer = UserDetail.objects.get(pk=request.session['userID'])
        context = {'details': articlereg.objects.filter(userid = quer), 'userName':quer.name}
        return render(request, self.template_name, context)


