from django.db import models
from django.db.models.signals import post_save
# Create your models here.

class user(models.Model):
      username=models.CharField(max_length=100)
      uniqueid=models.CharField(primary_key=True,max_length=100)
      password=models.CharField(max_length=16)

class profile(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    state=models.CharField(max_length=100,null=True)
    district=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    def __str__(self):
        return self.user.username
    
class cart(models.Model):
    cartref=models.ForeignKey(user,on_delete=models.CASCADE) 
    items=models.CharField(max_length=100,null=True)

class product(models.Model):
      producttype=models.CharField(max_length=30,null=True)
      name=models.CharField(max_length=200)
      image=models.ImageField()
      cost=models.CharField(max_length=50)
      details=models.CharField(max_length=200)

def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=profile(user=instance)
        user_profile.save()

def create_cart(sender,instance,created,**kwargs):
    if created:
        cart_ref=cart(cartref=instance)
        cart_ref.save()

post_save.connect(create_profile,sender=user)
post_save.connect(create_cart,sender=user)
