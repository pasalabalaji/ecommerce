import pandas as pd
import numpy as np
import json
import ast
from .models import *
from django.http import HttpResponse


import csv   

def create_pkl():
    try:
        data=product.objects.all()
        for i in data:
            fields=[str(i.pid),str(i.producttype),str(i.name),str(i.cost),str(i.details)]
            with open('data.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        
        products=pd.read_csv("data.csv")
        products=products.dropna()
        products=products.drop_duplicates()
        def make_string(obj):
            word=""
            for i in obj:
                i.replace(" ","")
                i.lower()
                word+=i
            return word

        products["type"]=products["type"].apply(make_string)
        products["name"]=products["name"].apply(make_string)
        products["details"]=products["details"].apply(make_string)
        
        products["tags"]=products["details"]+products["name"]+str(products["price"])+products["details"]

        preprocessedDf=products[["id","tags"]]
        preprocessedDf=preprocessedDf.dropna()

        preprocessedDf["tags"]=preprocessedDf["tags"].apply(lambda x:" ".join(x))
        preprocessedDf["tags"]=preprocessedDf["tags"].apply(lambda x:x.lower())
        return 1
    except Exception as e:
        print(e)
        return 0