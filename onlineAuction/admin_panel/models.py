from django.db import models

# Create your models here.
class banned_user(models.Model):
    userid=models.IntegerField()
    time=models.DateTimeField(auto_now=True)

