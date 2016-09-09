from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from signup.models import UserDetail
def index(request):
    template_name = 'portal/index.html'
    context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
    return render(request, template_name, context)
def admin_page(request):
	context = {'details': UserDetail.objects.all()}
	template_name='portal/admin_page.html'
	return render(request, template_name, context)

def delete_user(request,id):
	b = UserDetail.objects.get(pk=id)
	b.delete()
	return HttpResponseRedirect(reverse('portal:admin_page'))





