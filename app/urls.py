from django.urls import path,include
from .views import *


urlpatterns=[
    path('',login,name="login"),
    path('signup',signup,name="signup"),
    path('create_user',create_user),
    path('add',add),
    path('validate',login),
    path('logout_user',logout),
    path('upload_product',upload_product),
    path('sell_product',sell_product),
    path('index',login),
    path('search_product',search_product),
    path('user_profile',user_profile),
    path('complete_registration',complete_registration),
    path('upload_registration',upload_registration),
    path('show/navindex',show_index),
    path('show/checkout/navindex',show_index),
    path('show/checkout/addtocart/<str:pk>',add_to_cart),
    path('show/checkout/<str:pk>',checkout),
    path('show/<str:pk>',show_product),
    path('cart',cart),
    path('buy',buy),
    
]