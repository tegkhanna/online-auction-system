from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [

	url(r'^adminPage/$', views.adminPage, name='adminPage'),
	url(r'delete/(?P<id>\d+)/$', views.deleteUser, name='delete'),
	url(r'showArticles/(?P<userid>\d+)/deleteArticle/(?P<id>\d+)/$', views.deleteArticle, name='delete'),
	url(r'ban/(?P<id>\d+)/$', views.banUser, name='ban'),
	url(r'showArticles/(?P<id>\d+)/$', views.showArticleDetails, name='showArticles'),
    


    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^RegForm/$', views.RegForm.as_view(), name='RegForm'),
    url(r'^UserShowArticle/$', views.UserShowArticles.as_view(), name='userArticles'),
	url(r'^UserShowArticle/EditArticles/(?P<a_id>\d+)/$', views.EditArticle.as_view(), name='editArticles'),
]