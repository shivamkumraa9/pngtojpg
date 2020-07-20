from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode


from users.models import MyUser
from users.forms import LoginForm,PasswordValidationForm,CustomUserCreationForm
from users.tokens import account_activation_token

def userlogin(request):

	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				user = MyUser.objects.get(email = email)
				user = authenticate(request,username = user.username,password = password)
				if user:
					if not user.is_verified:
						send_activation_email(request,user)
						messages.error(request, 'Email not verified!. Verification email sended!')
					else:
						login(request,user)
						return redirect("users:profile")
				else:
					messages.error(request, 'Invalid Email/Password.')
			except MyUser.DoesNotExist:
				messages.error(request, 'Invalid Email/Password.')
	else:
		form = LoginForm()

	return render(request,"users/login.html",{"form":form})



def userregister(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			send_activation_email(request,user)
			messages.success(request, 'Account has been created but you need to verify your email.check inbox')
			return redirect("users:login")
	else:
		form = CustomUserCreationForm()
	return render(request,"users/register.html",{"form":form})



@login_required
def delete(request):
	if request.method == "POST":
		form = PasswordValidationForm(request.POST)

		if form.is_valid():
			password = form.cleaned_data['password']
			user = request.user
			user = authenticate(request,username = user.username,password = password)
			if user:
				user.delete()
				messages.success(request, 'Account has been deleted')
				return redirect("users:login")
			else:
				messages.error(request, 'Invalid Password')
	else:
		form = PasswordValidationForm()
	return render(request,"users/delete.html",{"form":form})


@login_required
def profile(request):
	return render(request,"users/profile.html")


@login_required
def userlogout(request):
	logout(request)
	messages.success(request, 'User has been logged out')
	return redirect("users:login")


def activate(request,uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, ('Your account have been confirmed.'))
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
    return redirect('users:login')



def send_activation_email(request,user):
	site = get_current_site(request).domain
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	token = account_activation_token.make_token(user)
	url = "http://" + site + reverse("users:activate",args = (uid,token))

	send_mail('Easy Jpg Email Verification',f'click here to confirm {url}.','testing@gmail.com',[user.email],fail_silently=False)
