from django.urls import path,include
from .views import *


urlpatterns=[
    path('',login,name="login"),
    path('signup',signup,name="signup"),
    path('create_user',create_user),
    path('add',add),
    path('validate',login),
    path('logout_user',login),
]