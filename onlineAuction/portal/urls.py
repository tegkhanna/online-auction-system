from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^RegForm/$', views.RegForm.as_view(), name='RegForm'),
    url(r'^article-register/$', views.RegArt, name='RegArt'),
]