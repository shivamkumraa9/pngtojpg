from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
	path("",views.index,name = "index"),
	path("convert/",views.convert,name = "user_convert"),
	path("api-convert/",views.api_convert,name = "api_convert"),
]