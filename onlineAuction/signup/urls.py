from django.conf.urls import url,include

from . import views


app_name = 'signup'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signUpPage/$', views.Signup.as_view(), name='signUpPage'),
    url(r'^LoginForm/$', views.LoginForm.as_view(), name='LoginForm'),
    url(r'^VisaForm/$', views.VisaForm.as_view(), name='VisaForm'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^resetpassword/$', views.PasswordRecover.as_view(), name='PasswordRecover'),
    url(r'^passwordchange/(?P<getlink>\w{0,50})/$', views.PasswordChanger.as_view(), name='PasswordChanger')



    #url(r'^login/$', views.login, name='login'),
    #url(r'^visa/$', views.visaReg, name='visaReg'),
]
