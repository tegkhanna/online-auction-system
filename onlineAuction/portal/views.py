from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from signup.models import UserDetail
from portal.models import banned_user
def index(request):
    template_name = 'portal/index.html'
    context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
    return render(request, template_name, context)
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





