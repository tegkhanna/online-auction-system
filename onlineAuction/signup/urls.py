from django.conf.urls import url

from . import views


app_name = 'signup'
urlpatterns = [
    url(r'^signUpPage/$', views.FormView.as_view(), name='signUpPage'),
    url(r'^signUp/$', views.signup, name='signUp'),
]