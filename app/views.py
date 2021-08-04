# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./fieldagent-app-01252fe62f76.json")
firebase_admin.initialize_app(cred)
db = firestore.client()




config = {
    "apiKey": "AIzaSyD7uYyEUdp0GIvqwXpdDjfzMD8q5NQRMvc",
    "authDomain": "telegram-a501e.firebaseapp.com",
    "databaseURL": "https://telegram-a501e-default-rtdb.firebaseio.com",
    "projectId": "telegram-a501e",
    "storageBucket": "telegram-a501e.appspot.com",
    "messagingSenderId": "279661330491",
    "appId": "1:279661330491:web:56d2b2d9fe993c32d39c1e",
    
}

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()





@login_required(login_url="/login/")
def index(request):

    if request.method == 'POST':
        state = request.POST['state']
        district = request.POST['district']
        date = request.POST['date']
        date_=date.split('-')
        date_org= date_[2]+'-'+date_[1]+'-'+date_[0]

        Marketing_staff_id = request.POST['Marketing_staff_id']
      


        docs_ref = db.collection('adminData').document(state).collection(district).document(date_org).collection(Marketing_staff_id)
        docs = docs_ref.get()
        list_dict=[]

        print(state)
        print(district)
        print(date_org)
        print(Marketing_staff_id)
        for doc in docs:
            list_dict.append(doc.to_dict())
            print(doc)
        
    
   

        html_template = loader.get_template( 'transactions.html' )
        return HttpResponse(html_template.render({'context':list_dict}, request))   
    
    # name=database.child('Data').child('name').get().val()

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'dashboard.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
