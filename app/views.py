from django.shortcuts import render
import json
from .models import *
from django.http import HttpResponse
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
import jwt,datetime
import random

def login(request):
    if(request.method=="POST"):
        form=MyForm(request.POST)
        if form.is_valid():
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
    if(request.COOKIES.get('user_cookie') is not None):
        form=MyForm()
        print("working")
        response=render(request,"login.html",{"form":form})
        response.delete_cookie('user_cookie')
        return response
    form=MyForm()
    return render(request,"login.html",{"form":form})


    



def signup(request):
    if(request.method=="POST"):
       form=SigninForm(request.POST)
       status=1
       print(form.is_valid())
       if(request.COOKIES.get('user_cookie') is not None): 
           form.is_valid()
           data=request.COOKIES["user_cookie"]
           decoded_token = jwt.decode(data, 'secret', 'HS256')
           if decoded_token["otp"]==form.cleaned_data["otp"]:
              user_obj=user(username=form.cleaned_data["username"],uniqueid=form.cleaned_data["mobileNumber"],password=form.cleaned_data["password"])
              user_obj.save()
              form=MyForm()
              message="You Had Registered Successfully,Please Login"
              response=render(request,"login.html",{"form":form,"message":message})
              response.delete_cookie("user_cookie")
              return response
           else:
              message="You have Entered an invalid valid OTP,Please Try Again..."
              return render(request,'signup.html',{"form":form,"status":status,"message":message})
         
       if form.is_valid():
            user_obj_name=user.objects.filter(username=form.cleaned_data["username"])
            user_obj_mail=user.objects.filter(uniqueid=form.cleaned_data["mobileNumber"])
            if len(user_obj_name)>=1:
                error=5
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            elif len(user_obj_mail)>=1:
                error=6
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            
            if "@" not in form.cleaned_data["mobileNumber"]:
                error=1
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            elif len(form.cleaned_data["username"])<6:
                error=2
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            elif len(form.cleaned_data["password"])<8:
                error=3
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            elif form.cleaned_data["password"]!=form.cleaned_data["confirmPassword"]:
                error=4
                status=0
                return render(request,'signup.html',{"form":form,"status":status,"error":error})
            subject = " OTP For signup of BCart  "
            otp=str(random.randint(1000,9999))
            message = "Your OTP for login is "+otp
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data["mobileNumber"]]
            send_mail( subject, message, email_from, recipient_list )
            payload={
                'email': form.cleaned_data["mobileNumber"],
                'password': form.cleaned_data["password"],
                'username': form.cleaned_data["username"],
                'otp': otp,
                'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                'iat':  datetime.datetime.utcnow()
            }
            encoded_token = jwt.encode(payload, 'secret', 'HS256')
            status=1
            response=render(request,'signup.html',{"form":form,"status":status})
            response.set_cookie('user_cookie',encoded_token)
            return response
       else:
            status=0
            return render(request,'signup.html',{"form":form,"status":status})
    else:
       status=0
       form=SigninForm()
       return render(request,'signup.html',{"form":form,"status":status})
    
def create_user(request):
    if(request.method=="POST"):
        data=json.loads(request.body)
        username=data["username"]
        ema_mob=data["uniqid"]
        password=data["password"]
        user_obj=user(username=username,uniqueid=ema_mob,password=password)
        user_obj.save()
        return HttpResponse("user created")
    else:
        return HttpResponse("restricted")

def add(request):
    if(request.method=="POST"):
        data=json.loads(request.body)
        obj=data["obj"]
        userobj=user.objects.get(uniqueid=data["details"])
        cartref=cart(cartref=userobj,items=obj)
        cartref.save()
        return HttpResponse("object added to cart")