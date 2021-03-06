from django.db import models
from signup import models as userdetails
from channels import Group

# Create your models here.
class banned_user(models.Model):
    userid=models.IntegerField()
    


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.article.userid.id, instance.article.id,ext)
    return '/'.join(['portal/static/portal/article_images', filename])

class articlereg(models.Model):
    def __str__(self):
        return str(self.id)
    userid=models.ForeignKey(userdetails.UserDetail)
    timestart=models.DateTimeField()
    articlename=models.CharField(max_length=40)
    status = models.CharField(max_length = 20 , default= "inactive")
    category=models.CharField(max_length=40)
    desc=models.CharField(max_length=150)
    minbid=models.FloatField(default=0.0)
    private = models.BooleanField(default = False)
    
class privateusers(models.Model):
    article = models.ForeignKey(articlereg)
    user = models.ForeignKey(userdetails.UserDetail)
    status = models.CharField(max_length = 20 , default= "inactive")

class articleimage(models.Model):
    def __str__(self):
        return str(self.image).split('/')[-1]
    article = models.ForeignKey(articlereg)
    image = models.ImageField(upload_to=content_file_name,default='article_images/'+str(id)+'.jpg')

class bids(models.Model):
    userid=models.ForeignKey(userdetails.UserDetail)
    articleid=models.ForeignKey(articlereg)
    highestbid=models.FloatField(default=0.0)



