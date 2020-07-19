from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
	path("login/",views.userlogin,name = "login"),
	path("logout/",views.userlogout,name = "logout"),
	path("register/",views.userregister,name = "register"),
	path("dashboard/",views.profile,name = "profile"),
	path("delete/",views.delete,name = "delete"),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]