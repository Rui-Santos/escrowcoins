from django.db import models
from datetime import datetime
#for user
from django.contrib.auth.models import User


# User model
class User(models.Model): 
    user = models.OneToOneField(User)


class Transaction(models.Model):
	'''
	Transaction Model
	'''
	user = models.ForeignKey('User')
	sender = models.EmailField(max_length=70,blank=False)
	buyer = models.EmailField(max_length=70,blank=False)
	escrower = models.EmailField(max_length=70,blank=False)
	added = models.DateTimeField(default=datetime.now, blank=True)
	helptext = models.TextField()

	
	@models.permalink
	def get_unique_url(self):
		'''
		direct link to transaction
		'''
		return('transaction', [str(self.id^0xABCDEFAB)])