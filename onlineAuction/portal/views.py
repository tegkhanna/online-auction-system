from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from signup.models import UserDetail
from portal.models import articlereg

from portal.models import banned_user
def adminPage(request):
	context = {'details': UserDetail.objects.all()}
	template_name='portal/adminPage.html'
	return render(request, template_name, context)

def deleteUser(request,id):
	b = UserDetail.objects.get(pk=id)
	b.delete()
	return HttpResponseRedirect(reverse('portal:adminPage'))
def banUser(request,id):
	if banned_user.objects.filter(userid=id).exists():
		pass
	else:
		ob=banned_user(userid=id)
		ob.save()
	return HttpResponseRedirect(reverse('portal:adminPage'))
def showArticleDetails(request,id):
    context = {'details': articlereg.objects.filter(userid=id)}
    template_name = 'portal/adminPageShowArticles.html'
    return render(request, template_name, context)

def deleteArticle(request,userid,id):
	b = articlereg.objects.get(pk=id)
	b.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







from .forms import *
class IndexView(generic.TemplateView):
    template_name = 'portal/index.html'
    
    def get(self, request, *args, **kwargs):
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
        return render(request, self.template_name, context)

   


class RegForm(generic.edit.FormView):
    form_class  = RegForm
    template_name = 'portal/articleForm.html'
    def get(self, request, *args, **kwargs):
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name, 'form':self.form_class}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])

            art=quer.articlereg_set.create( status = request.POST['status'],
                                        timestart=request.POST['timestart'],articlename=request.POST['articlename'],
                                        category=request.POST['category'],desc=request.POST['desc'],
                                        minbid=request.POST['minbid'])
            art.articleimage_set.create(image=request.FILES['image'])
            return HttpResponse("Article Successfully Registered.")
        except UserDetail.DoesNotExist:
            return HttpResponse("Article Successfully Registered.")

"""class EditArticle(generic.edit.FormView):
    form_class  = RegForm
    template_name = 'portal/articleForm.html'
    def get(self, request,a_id, *args, **kwargs):
        data = articlereg.objects.get(pk=a_id)
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name,
                     'form':self.form_class(initial = data)}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            art
            art=quer.articlereg_set.create( status = request.POST['status'],
                                        timestart=request.POST['timestart'],articlename=request.POST['articlename'],
                                        category=request.POST['category'],desc=request.POST['desc'],
                                        minbid=request.POST['minbid'])
            art.articleimage_set.create(image=request.FILES['image'])
            return HttpResponse("Article Successfully Registered.")
        except UserDetail.DoesNotExist:
            return HttpResponse("Article Successfully Registered.")"""


class UserShowArticles(generic.TemplateView):
    template_name = 'portal/usershowarticle.html'
    def get(self, request, *args, **kwargs):
        quer = UserDetail.objects.get(pk=request.session['userID'])
        context = {'details': articlereg.objects.filter(userid = quer), 'userName':quer.name}
        return render(request, self.template_name, context)
