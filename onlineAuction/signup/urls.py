from django.conf.urls import url

from . import views


app_name = 'signup'
urlpatterns = [
    url(r'^signUpPage/$', views.FormView.as_view(), name='signUpPage'),
    url(r'^LoginForm/$', views.LoginForm.as_view(), name='LoginForm'),
    url(r'^signUp/$', views.signup, name='signUp'),
    url(r'^login/$', views.login, name='login'),
]