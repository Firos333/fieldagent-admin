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
from django.contrib.auth.decorators import user_passes_test

cred = credentials.Certificate("./fieldagent-app-01252fe62f76.json")
firebase_admin.initialize_app(cred)
db = firestore.client()






# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()




@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login/")
def index(request):

    if request.method == 'POST':
        state = request.POST['state']
        district = request.POST['district']

        docs_ref = db.collection('users')
        docs = docs_ref.stream()
        list_dict=[]
        
        for doc in docs:
            dictionary =doc.to_dict()
            if dictionary['district']== district:
                list_dict.append(dictionary)
 


        html_template = loader.get_template( 'user_distrct.html' )
        return HttpResponse(html_template.render({'context':list_dict}, request)) 

    context = {}
    

    html_template = loader.get_template( 'dashboard.html' )
    return HttpResponse(html_template.render(context, request))

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login/")
def staffs(request):

 
    docs_ref = db.collection('users')
    docs = docs_ref.stream()
    list1=[]
    
    for doc in docs:
        dictionary =doc.to_dict()
        list1.append(dictionary)
        print(list1)


    html_template = loader.get_template( 'complete_users.html' )
    return HttpResponse(html_template.render({'context':list1}, request)) 

   


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login/")
def search(request):

   
    if request.method == 'POST':
        state = request.POST['state']
        name = request.POST['name1']
        district = request.POST['district']
        date = request.POST['date']
        date_=date.split('-')
        date_org= date_[2]+'-'+date_[1]+'-'+date_[0]

        Marketing_staff_id = request.POST['Marketing_staff_id']
      


        docs_ref = db.collection('adminData').document(state).collection(district).document(date_org).collection(Marketing_staff_id)
        docs = docs_ref.get()

        list_dict=[]

    
        for doc in docs:
            dictionary=doc.to_dict()
            dictionary['nickname']= name
            dictionary['state']= state
            dictionary['district']= district
            dictionary['date']= date

            list_dict.append(dictionary)
  
        
    
   

        html_template = loader.get_template( 'transactions.html' )
        return HttpResponse(html_template.render({'context':list_dict}, request))   
    

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
