from django.shortcuts import render
import json
from .models import *
from django.http import HttpResponse
from .forms import *
from django.conf import settings
from django.core.mail import send_mail


import jwt
from datetime import datetime, timedelta
import random
from django.shortcuts import redirect




def login(request):
    if(request.method=="POST"):
        form=MyForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user_obj=user.objects.filter(username=username,password=password)
            if len(user_obj)==0:
                error_message="User not found"
                return render(request,"login.html",{"form":form,"error_message":error_message})
            else:
                # payload={
                # 'username': username,
                # 'login_status': 1,
                # 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                # 'iat':  datetime.datetime.utcnow()
                # }
                payload = {
                'username': username,
                'login_status': 1,
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow()
                 }
                encoded_token = jwt.encode(payload, 'secret', 'HS256')
                user_searches=user_searchs.objects.filter(userobj=user.objects.get(username=username,password=password))
                search_key=""
                similar_id=[]
                for i in user_searches:
                    search_key+=" "+i.searchs
                    if search_key!="":
                       similar_id=create_pkl(search_key)
                if len(similar_id)==0:
                   response=render(request,'index.html')
                   response.set_cookie('user_cookie',encoded_token)
                else:
                    objs=[]
                    for i in similar_id:
                        objs.append(product.objects.get(pid=i))
                    count=len(ucart.objects.filter(cartref=user.objects.get(username=username)))
                    response=render(request,'index.html',{"objs": objs,"count":count})
                    response.set_cookie('user_cookie',encoded_token)
                return response
        else:
            return render(request,"login.html",{"form":form})
    if(request.COOKIES.get('user_cookie') is not None):
        form=MyForm()
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        if decoded_token["login_status"]==1:  
                user_searches=user_searchs.objects.filter(userobj=user.objects.get(username=decoded_token["username"]))
                search_key=""
                similar_id=[]
                if len(user_searches)>10:
                   user_searches=user_searches[len(user_searches)-10:len(user_searches)]
                for i in user_searches:
                    search_key+=" "+i.searchs
                    if search_key!="":
                       similar_id=create_pkl(search_key)
                if len(similar_id)==0:
                   response=render(request,'index.html')
                else:
                    objs=[]
                    for i in similar_id:
                        objs.append(product.objects.get(pid=i))
                    count=len(ucart.objects.filter(cartref=user.objects.get(username=decoded_token["username"])))
                    response=render(request,'index.html',{"objs": objs,"count":count})
                return response
          
    form=MyForm()
    return render(request,"login.html",{"form":form})


def logout(request):
    form=MyForm()
    response=render(request,"login.html",{"form":form})
    response.delete_cookie('user_cookie')
    return response  



def signup(request):
    if(request.method=="POST"):
       form=SigninForm(request.POST)
       status=1
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
    
def upload_product(request):
    if(request.COOKIES.get('user_cookie') is not None):
        productType=request.POST["productType"]
        productName=request.POST["productName"]
        productImageUrl=request.POST["productImage"]
        productCost=request.POST["productCost"]
        productDetails=request.POST["productDetails"]
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        pid=decoded_token["username"]+productName+productCost
        user_obj=user.objects.get(username=decoded_token["username"])
        pObj=product(user_product=user_obj,producttype=productType,name=productName,pid=pid,image=productImageUrl,cost=productCost,details=productDetails)
        pObj.save()
        message="Product is uploaded..."
        return render(request,"sellproduct.html",{"message":message})

def sell_product(request):
    if(request.COOKIES.get('user_cookie') is not None):
       return render(request,"sellproduct.html")

from .util import *

def search_product(request):
    if(request.COOKIES.get('user_cookie') is not None):
        productName=request.GET["product"]
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        uname=decoded_token["username"]
        searchs=user_searchs.objects.filter(searchs=productName)
        user_search=user_searchs.objects.filter(userobj=user.objects.get(username=uname).uniqueid)
        if len(user_search)>=10:
            for i in range(len(user_search)-9):
                    user_searchs.objects.filter(searchs=user_search[i].searchs,userobj=user_search[i].userobj).delete()
        if len(searchs)==0:
            searchobj=user_searchs(userobj=user.objects.get(username=uname),searchs=productName)
            searchobj.save()
        similar_id=create_pkl(productName)
        objs=[]
        for i in similar_id:
            objs.append(product.objects.get(pid=i))
        return render(request,"sr.html",{"objects":objs})
    else:
        return render(request,"login.html")

def user_profile(request):
    if(request.COOKIES.get('user_cookie') is not None):
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        uname=decoded_token["username"]
        user_obj=user.objects.get(username=uname)
        user_profile=profile.objects.filter(user=user_obj)
        orders=user_orders.objects.filter(ordered_user=user_obj)
        count=len(ucart.objects.filter(cartref=user.objects.get(username=uname)))
        if len(user_profile)==0:
           return render(request,"profile.html",{"user":user_obj,"status":0,"count":count}) 
        else:
           user_profile=profile.objects.get(user=user_obj)
           if len(orders)==0:
               return render(request,"profile.html",{"user":user_obj,"obj":user_profile,"status":1,"orders_message":0,"count":count})
           else:
               orders=user_orders.objects.filter(ordered_user=user_obj)
               return render(request,"profile.html",{"user":user_obj,"obj":user_profile,"status":1,"orders":orders,"orders_message":1,"count":count})  
    else:
        return render(request,"login.html")

def complete_registration(request):
    if(request.COOKIES.get('user_cookie') is not None):
        return render(request,"completeregistration.html")
    else:
        return render(request,"login.html")

def upload_registration(request):
    if(request.COOKIES.get('user_cookie') is not None):
        state=request.POST["state"]
        district=request.POST["district"]
        city=request.POST["city"]
        pincode=request.POST["pincode"]
        mobile_number=request.POST["mobileNumber"]
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        user_obj=user.objects.get(username=decoded_token["username"])
        pObj=profile(user=user_obj,state=state,district=district,city=city,pincode=pincode,mobile_number=mobile_number,premium="no")
        pObj.save()
        message="Registration Comleted..."
        return render(request,"completeregistration.html",{"message":message})
    else:
        return render(request,"login.html")

def show_product(request,pk):
    if(request.COOKIES.get('user_cookie') is not None):
       productobj=product.objects.get(pid=pk)
       return render(request,"productinfo.html",{"obj":productobj})
    else:
        return render(request,"login.html")

def show_index(request):
    if(request.COOKIES.get('user_cookie') is not None):
       return redirect("http://127.0.0.1:8000")
    else:
        return render(request,"login.html")

def checkout(request,pk):
    if(request.COOKIES.get('user_cookie') is not None):
        product_obj=product.objects.get(pid=pk)
        return render(request,"checkout.html",{"product":product_obj})
    else:
        return render(request,"login.html")

def add_to_cart(request,pk):
    if(request.COOKIES.get('user_cookie') is not None):
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        user_obj=user.objects.get(username=decoded_token["username"])
        product_obj=product.objects.get(pid=pk)
        cartobj=ucart(cartref=user_obj,item=product_obj)
        cartobj.save()          
        return redirect("http://127.0.0.1:8000/cart")
    else:
        return render(request,"login.html")

def cart(request):
    if(request.COOKIES.get('user_cookie') is not None):
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        user_obj=user.objects.get(username=decoded_token["username"])
        ucartobj=ucart.objects.filter(cartref=user_obj)
        cartitems=[]
        for i in ucartobj:
            cartitems.append(i.item)
        if len(ucartobj)==0:
           return render(request,"cart.html",{"status":0}) 
        else:
           return render(request,"cart.html",{"status":1,"cartitems":cartitems})
    else:
        return render(request,"login.html")
    



def buy(request):
    if(request.COOKIES.get('user_cookie') is not None):
        ordered_items=request.POST.getlist("options")
        if len(ordered_items)==0:
           return redirect("http://127.0.0.1:8000/cart")         
        data=request.COOKIES["user_cookie"]
        decoded_token = jwt.decode(data, 'secret', 'HS256')
        user_obj=user.objects.get(username=decoded_token["username"])
        ordersobj=[]
        totalCost=0
        for item in ordered_items:
            ordersobj.append(product.objects.get(pid=item))
            totalCost+=int(product.objects.get(pid=item).cost)
            user_order=user_orders(ordered_user=user_obj,ordered_item=product.objects.get(pid=item).name,order_id="EBUY"+str(get_date_time()).replace("-","").replace(" ","").replace(":","").replace(".",""),ordered_date=str(datetime.now().date()),expected_delivery=product.objects.get(pid=item).cost,order_status="Confirmed")
            user_order.save()  
            cartobj=ucart.objects.filter(item=product.objects.get(pid=item)).first()
            cartobj.delete()
        return render(request,"confirmation.html",{"orders":ordersobj,"totalCost":totalCost})
    else:
      return render(request,"login.html")
    

        

#DEC
#1st week
#11/12/23-sections 1 all years-monday
#12/12/23-sections 2 all years-tuesday
#13/12/23-sections 3 all years-wednesday
#14/12/23-sections 4 all years-thursday
#15/12/23-sections 5 all years-friday
#16/12/23-section 6 all years-saturday
#17/12/23-type of Event decision and date announcement-sunday
#2nd wek
#17/12/23 to 23/12/23 mid exams
#23/12/23-Event day
#3rd and 4th weeks
#sem exams
#5th week
#07/01/24-project expo announcement

