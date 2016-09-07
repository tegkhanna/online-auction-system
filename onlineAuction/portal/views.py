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