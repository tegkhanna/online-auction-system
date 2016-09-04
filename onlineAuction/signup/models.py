from django.db import models

# Create your models here.
class UserDetail(models.Model):
	def __str__(self):
		return self.email
	userID=models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	password=models.CharField(max_length=30)
	email=models.CharField(max_length=50)
    bidCoins= models.IntegerField(default=0)






