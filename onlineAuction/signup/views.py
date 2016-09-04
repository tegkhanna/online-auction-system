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


def signup(request):
    form = UserForm(request.POST)
    new_user = form.save(commit=False)

    try:
    	quer = UserDetail.objects.get(email=new_user.email)
    except UserDetail.DoesNotExist:
        quer = None

    if(quer == None):
        new_user.save()
    else:
        return HttpResponseRedirect(reverse('polls:index'))
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
   # return HttpResponseRedirect(reverse('polls:index'))