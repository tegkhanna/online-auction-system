from django import forms
from .models import *
class UserForm(forms.ModelForm):#user form pre build class
 #   def __init__(self, *args, **kwargs):
   #     super(UserForm, self).__init__(*args, **kwargs)
    #    self.fields['__all__'].required = True


    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
    	model = UserDetail
    	widgets = {'bidCoin':forms.HiddenInput()}
    	fields = '__all__'


class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)