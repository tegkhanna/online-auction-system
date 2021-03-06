from django.db import models

# Create your models here.
class UserDetail(models.Model):
	def __str__(self):
		return str(self.id)
	userName=models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	password=models.CharField(max_length=256)
	email=models.EmailField(max_length=50)
	interests = models.CharField(max_length=40, default = 'Vehicle', null = True)



class Visa(models.Model):
	def __str__(self):
		return str(self.id)
	userid=models.ForeignKey(UserDetail)
	visaNum = models.CharField(max_length = 10)
	expDate=models.DateTimeField()


class Admins(models.Model):
	def __str__(self):
		return str(self.id)
	userName=models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	password=models.CharField(max_length=256)

class PasswordRecovery(models.Model):
    def __str__(self):
        return str(self.id)
    userid=models.IntegerField()
    email=models.EmailField(max_length=50)
    link=models.CharField(max_length=50)

