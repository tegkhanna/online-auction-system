from django import forms
from .models import *

class RegForm(forms.Form):#user form pre build class
    
    timestart=forms.DateTimeField()
    articlename=forms.CharField(max_length=40)
    Choices=(('Book','Book'),('Vehicle','Vehicle'),('Coin or Stamp','Coin or Stamp'),('Antique','Antique'),
             ('Electronics','Electronics'),('Others','Others'))
    category=forms.ChoiceField(choices=Choices)
    desc=forms.CharField(max_length=150)
    minbid=forms.FloatField()
    image=forms.ImageField()

class EditRegForm(forms.Form):#user form pre build class
    timestart=forms.DateTimeField()
    articlename=forms.CharField(max_length=40)
    Choices=(('Book','Book'),('Vehicle','Vehicle'),('Coin or Stamp','Coin or Stamp'),('Antique','Antique'),
             ('Electronics','Electronics'),('Others','Others'))
    category=forms.ChoiceField(choices=Choices)
    desc=forms.CharField(max_length=150)
    minbid=forms.FloatField()
    image=forms.ImageField()

class BidPrice(forms.Form):
     highestbid = forms.FloatField()