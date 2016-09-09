from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^adminpage/$', views.admin_page, name='admin_page'),
	url(r'delete/(?P<id>\d+)/$', views.delete_user, name='delete'),
	
    

]