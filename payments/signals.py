from payments.models import Customer

from django.db.models.signals import pre_delete
from django.dispatch import receiver

import stripe

@receiver(pre_delete,sender = Customer)
def signal(sender,instance,**kwargs):
	stripe.Customer.delete(instance.customer)
