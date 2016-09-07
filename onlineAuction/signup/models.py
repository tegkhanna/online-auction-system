from django.db import models

# Create your models here.
class UserDetail(models.Model):
	def __str__(self):
		return str(self.id)
	userName=models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	password=models.CharField(max_length=30)
	email=models.CharField(max_length=50)
	bidCoins= models.IntegerField(default=0)

class Visa(models.Model):
	def __str__(self):
		return str(self.id)
	userid=models.ForeignKey(UserDetail)
	visaNum = models.CharField(max_length = 10)
	expDate=models.DateTimeField()




