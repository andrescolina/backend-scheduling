from django.conf.urls import url,include
from .views import (
	ListUser,
	LoginUser
)

urlpatterns =[
	url(r'^register', ListUser.as_view()),
	url(r'^login', LoginUser.as_view()),
]