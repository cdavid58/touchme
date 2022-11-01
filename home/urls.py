from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^$',Login,name="Login"),
	url(r'^Index/$',Index,name="Index"),
	url(r'^Download_Music/$',Download_Music,name="Download_Music"),
	url(r'^Restaurar/$',Restaurar,name="Restaurar"),
	url(r'^Client/$',Client,name="Client"),
	url(r'^Save_Music_Client/$',Save_Music_Client,name="Save_Music_Client"),
	url(r'^Delete_Song/$',Delete_Song,name="Delete_Song"),
	url(r'^Request_List_Song/$',Request_List_Song,name="Request_List_Song"),
]