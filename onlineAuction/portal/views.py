from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

from signup.models import UserDetail
from .forms import *
class IndexView(generic.TemplateView):
    template_name = 'portal/index.html'
    
    def get(self, request, *args, **kwargs):
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
        return render(request, self.template_name, context)
        


class RegForm(generic.edit.FormView):
    form_class  = RegForm
    template_name = 'portal/articleForm.html'


def RegArt(request):
    try:
        quer = UserDetail.objects.get(pk=request.session['userID'])

        quer.articlereg_set.create( status = request.POST['status'], 
        							timestart=request.POST['timestart'],articlename=request.POST['articlename'],
        							category=request.POST['category'],desc=request.POST['desc'],
        							minbid=request.POST['minbid'],image=request.POST['image'])
        return HttpResponse("Article Successfully Registered.")
    except UserDetail.DoesNotExist:
        return HttpResponse("Article Successfully Registered.")