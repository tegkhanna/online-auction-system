from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^adminPage/$', views.adminPage, name='adminPage'),
	url(r'delete/(?P<id>\d+)/$', views.deleteUser, name='delete'),
	url(r'ban/(?P<id>\d+)/$', views.banUser, name='ban'),
	
    

]