from django import forms
from .models import *

class RegForm(forms.Form):#user form pre build class
    status=forms.CharField(max_length=10)
    timestart=forms.DateTimeField()
    articlename=forms.CharField(max_length=40)
    category=forms.CharField(max_length=40)
    desc=forms.CharField(max_length=150)
    minbid=forms.FloatField()
    image=forms.ImageField()