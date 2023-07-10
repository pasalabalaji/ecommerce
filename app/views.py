from django.shortcuts import render
import json
from .models import *
from django.http import HttpResponse
from .forms import *
# Create your views here.

def login(request):
    if(request.method=="POST"):
        form=MyForm(request.POST)
        if form.is_valid():
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
    form=MyForm()
    return render(request,"login.html",{"form":form})

    



def signup(request):
    if(request.method=="POST"):
       form=SigninForm(request.POST)
       status=1
       if form.is_valid():
            return render(request,'signup.html',{"form":form,"status":status})
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