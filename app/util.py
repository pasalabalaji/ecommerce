import pandas as pd
import numpy as np
import json
import ast
from .models import *
from django.http import HttpResponse
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
from sklearn.feature_extraction.text import CountVectorizer
import csv   
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

def helper(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def create_pkl():
    try:
        # data=product.objects.all()
        # for i in data:
        #     fields=[str(i.pid),str(i.producttype),str(i.name),str(i.cost),str(i.details)]
        #     with open('data.csv', 'a') as f:
        #         writer = csv.writer(f)
        #         writer.writerow(fields)
        
        products=pd.read_csv("data.csv")
        products=products.dropna()
        products=products.drop_duplicates()
        data={
               "pid":"0",
              "type":"x",
              "name":"y",
              "price":"0",
              "details":"cotton shirt",
        }
        products=products._append(data,ignore_index=True)
        print(products)
        def make_string(obj):
            word=""
            for i in obj:
                i.replace(" ","")
                i.lower()
                word+=i
            return [word]

        products["type"]=products["type"].apply(make_string)
        products["name"]=products["name"].apply(make_string)

        products["details"]=products["details"].apply(lambda x:x.split())
        
        products["tags"]=products["details"]+products["name"]+products["type"]



        
        preprocessedDf=products[["pid","tags"]]
        preprocessedDf=preprocessedDf.dropna()
        
        
        preprocessedDf["tags"]=preprocessedDf["tags"].apply(lambda x:" ".join(x))
        preprocessedDf["tags"]=preprocessedDf["tags"].apply(lambda x:x.lower())
        preprocessedDf["tags"]=preprocessedDf["tags"].apply(lambda x:helper(x))
        
        cv=CountVectorizer(max_features=5000,stop_words="english")
        vectors=cv.fit_transform(preprocessedDf["tags"]).toarray()
        similarities=cosine_similarity(vectors)
       
        print(similarities)
        return 1
    except Exception as e:
        print(e)
        return 0