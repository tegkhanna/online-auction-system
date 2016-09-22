from django import forms
from .models import *
from signup.models import UserDetail
class RegForm(forms.Form):#user form pre build class

    timestart=forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD HH:MM:SS'}),label="Start date and time:")
    articlename=forms.CharField(max_length=40,label="Article Name:")
    Choices=(('Book','Book'),('Vehicle','Vehicle'),('Coin or Stamp','Coin or Stamp'),('Antique','Antique'),
             ('Electronics','Electronics'),('Others','Others'))
    category=forms.ChoiceField(choices=Choices)
    desc = forms.CharField(max_length=150, label="Description:")
    minbid = forms.FloatField(min_value=0, label="Minimum bid:")
    Users = []
    for names in UserDetail.objects.all():
        tup = (names ,names.name)
        Users.append(tup)
    private = forms.BooleanField(initial = True)
    Select_Users = forms.MultipleChoiceField(required = False, widget = forms.CheckboxSelectMultiple, choices = Users)
    image=forms.ImageField()


class EditRegForm(forms.Form):#user form pre build class
    timestart=forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'placeholder':'YYYY-MM-DD HH:MM:SS'}),label="Start date and time:")
    articlename=forms.CharField(max_length=40,label="Article Name:")
    Choices=(('Book','Book'),('Vehicle','Vehicle'),('Coin or Stamp','Coin or Stamp'),('Antique','Antique'),
             ('Electronics','Electronics'),('Others','Others'))
    category=forms.ChoiceField(choices=Choices)
    desc=forms.CharField(max_length=150,label="Description:")
    minbid=forms.FloatField(min_value=0,label="Minimum bid:")
    image=forms.ImageField()

class BidPrice(forms.Form):
     highestbid = forms.FloatField(min_value=0.0)