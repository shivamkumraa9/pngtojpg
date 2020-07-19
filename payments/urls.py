from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
	path("add/",views.add,name = "add"),
	path("success/<str:session_id>/",views.success,name = "success"),
	path("fail/",views.fail,name = "fail"),
]