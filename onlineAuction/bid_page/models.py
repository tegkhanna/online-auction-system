from django.db import models
from signup import models as userdetails
from articles import models as articledetails
# Create your models here.

class bids(models.Model):
    userid=models.ForeignKey(userdetails.UserDetail)
    articleid=models.ForeignKey(articledetails.articlereg)
    highestbid=models.FloatField(default=0)