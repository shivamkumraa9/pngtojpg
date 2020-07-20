from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseNotFound,HttpResponse

from payments.models import Customer,Intent
from payments.forms import AmountForm

import stripe


stripe.api_key = 'sk_test_51GzkYJAkCUXrZtDnbcFTP9srjGSW6Hp15wcNVjsQO5sSJQeEhLwvISsZgESjCqULg9bySvT8JPykaCMe3pd1kUxC00Uvkv2jDx'
endpoint_secret = 'whsec_...'



@login_required
def add(request):
	if request.method == "POST":
		form = AmountForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data['amount'] * 100
			session = stripe.checkout.Session.create(
			  payment_method_types=['card'],
			  customer = request.user.customer.customer,
			  line_items=[{
			    'price_data': {
			      'currency': 'usd',
			      'product': 'prod_HYt5zdS2dILB5a',
			      'unit_amount': amount,
			    },
			    'quantity': 1,
			  }],
		 
			  mode='payment',
			  success_url='http://pngtojpg.herokuapp.com/payments/success/{CHECKOUT_SESSION_ID}/',
			  cancel_url='http://pngtojpg.herokuapp.com/payments/fail/',
			)
			return render(request,"payments/add.html",{"CHECKOUT_SESSION_ID":session['id']})

	else:
		form = AmountForm()
	return render(request,"payments/add.html",{"form":form})

   
def success(request,session_id):
	session = stripe.checkout.Session.retrieve(session_id)
	intent = stripe.PaymentIntent.retrieve(session['payment_intent'])
	customer = intent['customer']
	amount = intent['amount'] / 100
	try:
		Intent.objects.get(intent = intent)
		return HttpResponseNotFound("404")
	except:
		c = Customer.objects.get(customer = customer)
		c.balance += (amount*10)
		c.save()
		Intent.objects.create(intent = intent)
		return render(request,"payments/success.html")


def fail(request):
	return render(request,"payments/fail.html")




@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # session = stripe.checkout.Session.retrieve(session_id)
    intent = stripe.PaymentIntent.retrieve(session['payment_intent'])
    customer = intent['customer']
    amount = intent['amount'] / 100

    c = Customer.objects.get(customer = customer)
    c.balance += (amount*10)
    c.save()

  return HttpResponse(status=200)