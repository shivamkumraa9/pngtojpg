from django.db import models
from users.models import MyUser


class Customer(models.Model):
	user = models.OneToOneField(MyUser,on_delete = models.CASCADE)
	customer = models.CharField(max_length = 50)
	balance = models.IntegerField(default = 50)
	token = models.CharField(max_length=40)
	def __str__(self):
		return self.user.username


class Intent(models.Model):
	intent = models.TextField(unique = True)

	def __str__(self):
		return self.intent