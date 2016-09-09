from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [

	url(r'^adminPage/$', views.adminPage, name='adminPage'),
	url(r'delete/(?P<id>\d+)/$', views.deleteUser, name='delete'),
	url(r'ban/(?P<id>\d+)/$', views.banUser, name='ban'),
	
    


    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^RegForm/$', views.RegForm.as_view(), name='RegForm'),
    url(r'^article-register/$', views.RegArt, name='RegArt'),

]