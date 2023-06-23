from django.db import models

# Create your models here.

class user(models.Model):
      username=models.CharField(max_length=100)
      uniqueid=models.CharField(primary_key=True,max_length=100)
      password=models.CharField(max_length=16)

class profile(models.Model):
    user=models.OneToOneField(user,on_delete=models.CASCADE)
    state=models.CharField(max_length=100,null=True)
    district=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    def __str__(self):
        return self.user.username
    
class cart(models.Model):
    cartref=models.OneToOneField(user,on_delete=models.CASCADE) 
    items=models.CharField(max_length=100,null=True)

class product(models.Model):
      producttype=models.CharField(max_length=30,null=True)
      name=models.CharField(max_length=200)
      image=models.ImageField()
      cost=models.CharField(max_length=50)
      details=models.CharField(max_length=200)
