from django.db import models
from signup import models as userdetails

# Create your models here.
class banned_user(models.Model):
    userid=models.IntegerField()
    


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.userid.id, instance.userid.articlereg_set.count() + 1,ext)
    return '/'.join(['article_images', filename])

class articlereg(models.Model):
    def __str__(self):
        return str(self.id)
    userid=models.ForeignKey(userdetails.UserDetail)
    status=models.CharField(max_length=10)
    timestart=models.DateTimeField()
    articlename=models.CharField(max_length=40)
    category=models.CharField(max_length=40)
    desc=models.CharField(max_length=150)
    minbid=models.FloatField(default=0.0)
    image=models.ImageField(upload_to=content_file_name,default='article_images/'+str(id)+'.jpg')
class bids(models.Model):
    userid=models.ForeignKey(userdetails.UserDetail)
    articleid=models.ForeignKey(articlereg)
    highestbid=models.FloatField(default=0.0)