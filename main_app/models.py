from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Treasure(models.Model):
	name = models.CharField(max_length=100)
	value = models.DecimalField(max_digits=10, decimal_places=2)
	material = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	# user = models.ForeignKey(User)
	def __str__(self):
		return self.name