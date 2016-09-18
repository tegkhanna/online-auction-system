from django.conf.urls import url

from . import views

app_name = 'portal'

urlpatterns = [

    url(r'^adminPage/$', views.AdminIndexView.as_view(), name='adminPage'),
    url(r'delete/(?P<id>\d+)/$', views.AdminIndexView.deleteUser, name='delete'),
    url(r'ban/(?P<id>\d+)/$', views.AdminIndexView.banUser, name='ban'),

    url(r'showArticles/(?P<userid>\d+)/deleteArticle/(?P<id>\d+)/$', views.ArticleView.deleteArticle, name='delete'),
    url(r'showArticles/(?P<id>\d+)/$', views.ArticleView.as_view(), name='showArticles'),

    url(r'activeArticles/$', views.ActiveBidView.as_view(), name='activeArticles'),

    url(r'recentArticles/$', views.RecentBidView.as_view(), name='recentArticles'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^RegForm/$', views.RegForm.as_view(), name='RegForm'),
    url(r'^UserShowArticle/$', views.UserShowArticles.as_view(), name='userArticles'),
    url(r'^UserShowArticle/EditArticles/(?P<a_id>\d+)/$', views.EditArticle.as_view(), name='editArticles'),
    url(r'^activeArticles/BidPage/(?P<a_id>\d+)/$', views.Bid.as_view(), name='Bid'),
    url(r'^activeArticles/BidPage/SoldPage/(?P<a_id>\d+)/$', views.Bid.sold, name='Bid'),
    url(r'^SoldBids/$', views.BidsSoldView.as_view(), name='soldArticles'),
    url(r'^WonBids/$', views.BidsWonView.as_view(), name='wonArticles'),

]