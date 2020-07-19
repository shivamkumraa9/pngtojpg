from users.models import MyUser
from django.db.models.signals import post_save

from django.dispatch import receiver
from payments.models import Customer

import stripe
import binascii
import os

@receiver(post_save,sender = MyUser)
def signal(sender,instance,created,**kwargs):
	if created:
		c = Customer.objects.create(user = instance,
									customer = stripe.Customer.create()['id'],
									token = binascii.hexlify(os.urandom(20)).decode())
