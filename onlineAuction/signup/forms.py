from django import forms
from .models import *
class UserForm(forms.ModelForm):#user form pre build class
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
    	model = UserDetail
    	fields = '__all__'


class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput)

class VisaForm(forms.Form):#user form pre build class
	visaNum = forms.CharField(max_length = 10,label="Visa Number")
	expDate= forms.DateTimeField(label="Expiry Date:",widget=forms.widgets.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD'}))