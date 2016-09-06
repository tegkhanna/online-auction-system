from django.db import models
from signup import models as userdetails
# Create your models here.
class articlereg(models.Model):
    userid=models.ForeignKey(userdetails.UserDetail)
    status=models.CharField(max_length=10)
    timestart=models.DateTimeField()
    articlename=models.CharField(max_length=40)
    category=models.CharField(max_length=40)
    desc=models.CharField(max_length=150)
    minbid=models.IntegerField(default=0)
    image=models.ImageField(upload_to='article_images/',default='article_images/'+str(self.id)+'.jpg')




