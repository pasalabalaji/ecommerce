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
from datetime import datetime

def get_date_time():
    return datetime.now()

def helper(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def transform(vectors):
    cv=CountVectorizer(max_features=5000,stop_words="english")
    return cv.fit_transform(vectors).toarray()

def create_pkl(product_search):
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
        data={
               "pid":"0",
              "type":"x",
              "name":"y",
              "price":"0",
              "details": product_search,
        }
        products=products._append(data,ignore_index=True)
        
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
        
        
        vectors=transform(preprocessedDf["tags"])
        # vectors=cv.fit_transform(preprocessedDf["tags"]).toarray()
        similarities=cosine_similarity(vectors)
       
        similarity=similarities[len(similarities)-1]
        similarity=sorted(list(enumerate(similarity[:len(similarity)-1])),reverse=True,key=lambda x:x[1])
        # print(preprocessedDf["pid"][similarity[0][0]])
        similar_products=[]
        count=0
        for i in similarity:
            if count>9:
               break
            elif i[1]!=0:
                similar_products.append(preprocessedDf["pid"][i[0]])
                count+=1
        return similar_products
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong...please try again later...")