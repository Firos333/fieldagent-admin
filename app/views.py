# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import messages
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
import pandas
from datetime import date as datte, timedelta

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
   


    html_template = loader.get_template( 'complete_users.html' )
    return HttpResponse(html_template.render({'context':list1}, request)) 

   


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login/")
def search(request):

   
    if request.method == 'POST':
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        if 'time_true' in request.POST:
            
            state = request.POST['state']
            time = request.POST['time_true']
            name = request.POST['name']
            district = request.POST['district']
            date = request.POST['date']
            Marketing_staff_id = request.POST['Marketing_staff_id']
            date_time = str(date)+' '+str(time)


            Data_dict = {"nickname": name, 
                    "state": state, "district": district,
                     "date1": date1,
                     "date2": date2,
                     }
            Data_list=[]
            Data_list.append(Data_dict)
            col_ref = db.collection('adminData').document(state).collection(district).document(date).collection(Marketing_staff_id)
            col_reff = col_ref.get()

            state_dist= state+': '+ district
            
            col_ref2 = db.collection('fielddata').document(state_dist).collection(Marketing_staff_id)
            print(col_ref2)

            for item in col_reff:
                if item.id == time:
                    doc = col_ref.document(item.id)
                    doc2 = col_ref2.document(date_time)

                    field_updates = {"isVerified": False}
                    doc.update(field_updates)
                    doc2.update(field_updates)

            date_1=date1.split('-')
            date_start= date_1[2]+'-'+date_1[1]+'-'+date_1[0]

            date_2=date2.split('-')
            date_end= date_2[2]+'-'+date_2[1]+'-'+date_2[0]

            sdate = datte(int(date_1[0]),int(date_1[1]),int(date_1[2]))   # start date
            edate = datte(int(date_2[0]),int(date_2[1]),int(date_2[2])) 
           
            delta = edate - sdate  
            list_dict=[]
            Total_num = 0
            Total_Verified = 0
            Total_paid = 0
            Totl_Paid_amount = 0
            Totl_UnPaid_amount= 0
            Total_Ver_Paid_amount=0
            Total_Ver_Unpaid_amount=0
            for i in range(delta.days + 1):
                day = str(sdate + timedelta(days=i))
                day_list=day.split('-')
                day_split= day_list[2]+'-'+day_list[1]+'-'+day_list[0]
                        
                Marketing_staff_id = request.POST['Marketing_staff_id']
        


                docs_ref = db.collection('adminData').document(state).collection(district).document(day_split).collection(Marketing_staff_id)
                docs = docs_ref.get()
        
                

            
                for doc in docs:
                    Total_num =Total_num+1
                    dictionary=doc.to_dict()
                    dictionary['nickname']= name
                    dictionary['state']= state
                    dictionary['district']= district
                    dictionary['id_user']= Marketing_staff_id
                    dictionary['date1']= date1
                    dictionary['date2']= date2

                    list_dict.append(dictionary)
                    is_verified =dictionary.get("isVerified")
                    is_Paid =dictionary.get("isPaid")
                    agent_amount = dictionary.get("Agent_charge")
                    if is_verified:
                        Total_Verified= Total_Verified+1
                    if is_Paid:
                        Total_paid= Total_paid+1
                        Totl_Paid_amount=Totl_Paid_amount+agent_amount
                    if not is_Paid:
              
                        Totl_UnPaid_amount=Totl_UnPaid_amount+agent_amount

                    if is_verified==True and is_Paid==True:
                        Total_Ver_Paid_amount = Total_Ver_Paid_amount+agent_amount

                    if is_verified==True and is_Paid==False:
                        Total_Ver_Unpaid_amount = Total_Ver_Unpaid_amount+agent_amount
                    
            
            
               
            Total_unVer_Paid_amount=Total_paid-Total_Ver_Paid_amount
        
            Payment_dict = {"Total_Verified": Total_Verified, 
                        "Total_paid": Total_paid, "Totl_Paid_amount": Totl_Paid_amount,
                        "Total_Ver_Paid_amount": Total_Ver_Paid_amount,
                        "Total_Ver_Unpaid_amount": Total_Ver_Unpaid_amount,
                        "Total_num": Total_num,
                        "Totl_UnPaid_amount": Totl_UnPaid_amount,
                        }
            list_payment=[]
            list_payment.append(Payment_dict)
              
         
            html_template = loader.get_template( 'transactions.html' )
            return HttpResponse(html_template.render({'context':list_dict,'context0':Data_list,'context1':list_payment}, request))  

        if 'time_false' in request.POST:
            state = request.POST['state']
            time = request.POST['time_false']
            name = request.POST['name']
            district = request.POST['district']
            date = request.POST['date']
            date_time = str(date)+' '+str(time)
  

            Marketing_staff_id = request.POST['Marketing_staff_id']
            Data_dict = {"nickname": name, 
                    "state": state, "district": district,
                     "date1": date1,
                     "date2": date2,
                     }
            Data_list=[]
            Data_list.append(Data_dict)

            col_ref = db.collection('adminData').document(state).collection(district).document(date).collection(Marketing_staff_id)
            col_reff = col_ref.get()

            state_dist= state+': '+ district
            
            col_ref2 = db.collection('fielddata').document(state_dist).collection(Marketing_staff_id)
            

            for item in col_reff:
                if item.id == time:
                    doc = col_ref.document(item.id)
                    doc2 = col_ref2.document(date_time)

                    field_updates = {"isVerified": True}
                    doc.update(field_updates)
                    doc2.update(field_updates)

            date_1=date1.split('-')
            date_start= date_1[2]+'-'+date_1[1]+'-'+date_1[0]

            date_2=date2.split('-')
            date_end= date_2[2]+'-'+date_2[1]+'-'+date_2[0]

            sdate = datte(int(date_1[0]),int(date_1[1]),int(date_1[2]))   # start date
            edate = datte(int(date_2[0]),int(date_2[1]),int(date_2[2])) 
           
            delta = edate - sdate  
            list_dict=[]
            Total_num = 0
            Total_Verified = 0
            Total_paid = 0
            Totl_Paid_amount = 0
            Totl_UnPaid_amount= 0
            Total_Ver_Paid_amount=0
            Total_Ver_Unpaid_amount=0
            for i in range(delta.days + 1):
                day = str(sdate + timedelta(days=i))
                day_list=day.split('-')
                day_split= day_list[2]+'-'+day_list[1]+'-'+day_list[0]
                        
                Marketing_staff_id = request.POST['Marketing_staff_id']
        


                docs_ref = db.collection('adminData').document(state).collection(district).document(day_split).collection(Marketing_staff_id)
                docs = docs_ref.get()
        
                

            
                for doc in docs:
                    Total_num =Total_num+1
                    dictionary=doc.to_dict()
                    dictionary['nickname']= name
                    dictionary['state']= state
                    dictionary['district']= district
                    dictionary['id_user']= Marketing_staff_id
                    dictionary['date1']= date1
                    dictionary['date2']= date2

                    list_dict.append(dictionary)
                    is_verified =dictionary.get("isVerified")
                    is_Paid =dictionary.get("isPaid")
                    agent_amount = dictionary.get("Agent_charge")
                    if is_verified:
                        Total_Verified= Total_Verified+1
                    if is_Paid:
                        Total_paid= Total_paid+1
                        Totl_Paid_amount=Totl_Paid_amount+agent_amount
                    if not is_Paid:
              
                        Totl_UnPaid_amount=Totl_UnPaid_amount+agent_amount

                    if is_verified==True and is_Paid==True:
                        Total_Ver_Paid_amount = Total_Ver_Paid_amount+agent_amount

                    if is_verified==True and is_Paid==False:
                        Total_Ver_Unpaid_amount = Total_Ver_Unpaid_amount+agent_amount
                    
            
            
               
            Total_unVer_Paid_amount=Total_paid-Total_Ver_Paid_amount
        
            Payment_dict = {"Total_Verified": Total_Verified, 
                        "Total_paid": Total_paid, "Totl_Paid_amount": Totl_Paid_amount,
                        "Total_Ver_Paid_amount": Total_Ver_Paid_amount,
                        "Total_Ver_Unpaid_amount": Total_Ver_Unpaid_amount,
                        "Total_num": Total_num,
                        "Totl_UnPaid_amount": Totl_UnPaid_amount,
                        }
            list_payment=[]
            list_payment.append(Payment_dict)
         

            html_template = loader.get_template( 'transactions.html' )
            return HttpResponse(html_template.render({'context':list_dict,'context0':Data_list,'context1':list_payment}, request))    
        
        if 'time_pay_true' in request.POST:
            state = request.POST['state']
            time = request.POST['time_pay_true']
            name = request.POST['name']
            district = request.POST['district']
            date = request.POST['date']
            Marketing_staff_id = request.POST['Marketing_staff_id']
            date_time = str(date)+' '+str(time)
            Data_dict = {"nickname": name, 
                    "state": state, "district": district,
                     "date1": date1,
                     "date2": date2,
                     }
            Data_list=[]
            Data_list.append(Data_dict)

            col_ref = db.collection('adminData').document(state).collection(district).document(date).collection(Marketing_staff_id)
            col_reff = col_ref.get()

            state_dist= state+': '+ district
            
            col_ref2 = db.collection('fielddata').document(state_dist).collection(Marketing_staff_id)
            # col_reff2 = col_ref2.get()

            for item in col_reff:
                if item.id == time:
                    doc = col_ref.document(item.id)
                    doc2 = col_ref2.document(date_time)

                    field_updates = {"isPaid": False}
                    doc.update(field_updates)
                    doc2.update(field_updates)

            date_1=date1.split('-')
            date_start= date_1[2]+'-'+date_1[1]+'-'+date_1[0]

            date_2=date2.split('-')
            date_end= date_2[2]+'-'+date_2[1]+'-'+date_2[0]

            sdate = datte(int(date_1[0]),int(date_1[1]),int(date_1[2]))   # start date
            edate = datte(int(date_2[0]),int(date_2[1]),int(date_2[2])) 
           
            delta = edate - sdate  
            list_dict=[]
            Total_num = 0
            Total_Verified = 0
            Total_paid = 0
            Totl_Paid_amount = 0
            Totl_UnPaid_amount= 0
            Total_Ver_Paid_amount=0
            Total_Ver_Unpaid_amount=0
            for i in range(delta.days + 1):
                day = str(sdate + timedelta(days=i))
                day_list=day.split('-')
                day_split= day_list[2]+'-'+day_list[1]+'-'+day_list[0]
                        
                Marketing_staff_id = request.POST['Marketing_staff_id']
        


                docs_ref = db.collection('adminData').document(state).collection(district).document(day_split).collection(Marketing_staff_id)
                docs = docs_ref.get()
        
                

            
                for doc in docs:
                    Total_num =Total_num+1
                    dictionary=doc.to_dict()
                    dictionary['nickname']= name
                    dictionary['state']= state
                    dictionary['district']= district
                    dictionary['id_user']= Marketing_staff_id
                    dictionary['date1']= date1
                    dictionary['date2']= date2

                    list_dict.append(dictionary)
                    is_verified =dictionary.get("isVerified")
                    is_Paid =dictionary.get("isPaid")
                    agent_amount = dictionary.get("Agent_charge")
                    if is_verified:
                        Total_Verified= Total_Verified+1
                    if is_Paid:
                        Total_paid= Total_paid+1
                        Totl_Paid_amount=Totl_Paid_amount+agent_amount
                    if not is_Paid:
              
                        Totl_UnPaid_amount=Totl_UnPaid_amount+agent_amount

                    if is_verified==True and is_Paid==True:
                        Total_Ver_Paid_amount = Total_Ver_Paid_amount+agent_amount

                    if is_verified==True and is_Paid==False:
                        Total_Ver_Unpaid_amount = Total_Ver_Unpaid_amount+agent_amount
                    
            
            
               
            Total_unVer_Paid_amount=Total_paid-Total_Ver_Paid_amount
        
            Payment_dict = {"Total_Verified": Total_Verified, 
                        "Total_paid": Total_paid, "Totl_Paid_amount": Totl_Paid_amount,
                        "Total_Ver_Paid_amount": Total_Ver_Paid_amount,
                        "Total_Ver_Unpaid_amount": Total_Ver_Unpaid_amount,
                        "Total_num": Total_num,
                        "Totl_UnPaid_amount": Totl_UnPaid_amount,
                        }
            list_payment=[]
            list_payment.append(Payment_dict)
              
            
            html_template = loader.get_template( 'transactions.html' )
            return HttpResponse(html_template.render({'context':list_dict,'context0':Data_list,'context1':list_payment}, request))  

        if 'time_pay_false' in request.POST:
            state = request.POST['state']
            print(state)
            time = request.POST['time_pay_false']
            name = request.POST['name']
            district = request.POST['district']
            date = request.POST['date']
            Marketing_staff_id = request.POST['Marketing_staff_id']
            date_time = str(date)+' '+str(time)

            col_ref = db.collection('adminData').document(state).collection(district).document(date).collection(Marketing_staff_id)
            col_reff = col_ref.get()

            state_dist= state+': '+ district
            
            col_ref2 = db.collection('fielddata').document(state_dist).collection(Marketing_staff_id)
            # col_reff2 = col_ref2.get()

            for item in col_reff:
                if item.id == time:
                    doc = col_ref.document(item.id)
                    doc2 = col_ref2.document(date_time)

                    field_updates = {"isPaid": True}
                    doc.update(field_updates)
                    doc2.update(field_updates)

            
            if date1 == '' or date2 == '':
                messages.info(request,'No items available for this date, pls give valid date range')
                html_template = loader.get_template( 'transactions.html' )
                return HttpResponse(html_template.render({'context':''}, request)) 
            
            
            date_1=date1.split('-')
            date_start= date_1[2]+'-'+date_1[1]+'-'+date_1[0]

            date_2=date2.split('-')
            date_end= date_2[2]+'-'+date_2[1]+'-'+date_2[0]

            sdate = datte(int(date_1[0]),int(date_1[1]),int(date_1[2]))   # start date
            edate = datte(int(date_2[0]),int(date_2[1]),int(date_2[2])) 
           
            delta = edate - sdate  
            list_dict=[]
            Total_num = 0
            Total_Verified = 0
            Total_paid = 0
            Totl_Paid_amount = 0
            Totl_UnPaid_amount= 0
            Total_Ver_Paid_amount=0
            Total_Ver_Unpaid_amount=0
            for i in range(delta.days + 1):
                day = str(sdate + timedelta(days=i))
                day_list=day.split('-')
                day_split= day_list[2]+'-'+day_list[1]+'-'+day_list[0]
                        
                Marketing_staff_id = request.POST['Marketing_staff_id']
        


                docs_ref = db.collection('adminData').document(state).collection(district).document(day_split).collection(Marketing_staff_id)
                docs = docs_ref.get()
        
                

            
                for doc in docs:
                    Total_num =Total_num+1
                    dictionary=doc.to_dict()
                    dictionary['nickname']= name
                    dictionary['state']= state
                    dictionary['district']= district
                    dictionary['id_user']= Marketing_staff_id
                    dictionary['date1']= date1
                    dictionary['date2']= date2

                    list_dict.append(dictionary)
                    is_verified =dictionary.get("isVerified")
                    is_Paid =dictionary.get("isPaid")
                    agent_amount = dictionary.get("Agent_charge")
                    if is_verified:
                        Total_Verified= Total_Verified+1
                    if is_Paid:
                        Total_paid= Total_paid+1
                        Totl_Paid_amount=Totl_Paid_amount+agent_amount
                    if not is_Paid:
              
                        Totl_UnPaid_amount=Totl_UnPaid_amount+agent_amount

                    if is_verified==True and is_Paid==True:
                        Total_Ver_Paid_amount = Total_Ver_Paid_amount+agent_amount

                    if is_verified==True and is_Paid==False:
                        Total_Ver_Unpaid_amount = Total_Ver_Unpaid_amount+agent_amount
                    
            
            
               
            Total_unVer_Paid_amount=Total_paid-Total_Ver_Paid_amount
        
            Payment_dict = {"Total_Verified": Total_Verified, 
                        "Total_paid": Total_paid, "Totl_Paid_amount": Totl_Paid_amount,
                        "Total_Ver_Paid_amount": Total_Ver_Paid_amount,
                        "Total_Ver_Unpaid_amount": Total_Ver_Unpaid_amount,
                        "Total_num": Total_num,
                        "Totl_UnPaid_amount": Totl_UnPaid_amount,
                        }
            list_payment=[]
            list_payment.append(Payment_dict)
              
            Data_dict = {"nickname": name, 
                    "state": state, "district": district,
                     "date1": date1,
                     "date2": date2,
                     }
            Data_list=[]
            Data_list.append(Data_dict)
            html_template = loader.get_template( 'transactions.html' )
            return HttpResponse(html_template.render({'context':list_dict,'context0':Data_list,'context1':list_payment}, request))    

        if 'name1' in request.POST:
            state = request.POST['state']

            name = request.POST['name1']
            district = request.POST['district']
            date1 = request.POST['date1']
    
            date2 = request.POST['date2']
            Data_dict = {"nickname": name, 
                    "state": state, "district": district,
                     "date1": date1,
                     "date2": date2,
                     }
            Data_list=[]
            Data_list.append(Data_dict)

            if date1 == '' or date2 == '':
                messages.info(request,'No items available for this dateb range, pls give valid date range')
                html_template = loader.get_template( 'transactions.html' )
                return HttpResponse(html_template.render({'context0':Data_list}, request)) 
            
            
            date_1=date1.split('-')
            date_start= date_1[2]+'-'+date_1[1]+'-'+date_1[0]

            date_2=date2.split('-')
            date_end= date_2[2]+'-'+date_2[1]+'-'+date_2[0]

            sdate = datte(int(date_1[0]),int(date_1[1]),int(date_1[2]))   # start date
            edate = datte(int(date_2[0]),int(date_2[1]),int(date_2[2])) 
           
            delta = edate - sdate  
            list_dict=[]
            Total_num = 0
            Total_Verified = 0
            Total_paid = 0
            Totl_Paid_amount = 0
            Totl_UnPaid_amount= 0
            Total_Ver_Paid_amount=0
            Total_Ver_Unpaid_amount=0
            for i in range(delta.days + 1):
                day = str(sdate + timedelta(days=i))
                day_list=day.split('-')
                day_split= day_list[2]+'-'+day_list[1]+'-'+day_list[0]
                        
                Marketing_staff_id = request.POST['Marketing_staff_id']
        


                docs_ref = db.collection('adminData').document(state).collection(district).document(day_split).collection(Marketing_staff_id)
                docs = docs_ref.get()
        
                

            
                for doc in docs:
                    Total_num =Total_num+1
                    dictionary=doc.to_dict()
                    dictionary['nickname']= name
                    dictionary['state']= state
                    dictionary['district']= district
                    dictionary['id_user']= Marketing_staff_id
                    dictionary['date1']= date1
                    dictionary['date2']= date2

                    list_dict.append(dictionary)
                    is_verified =dictionary.get("isVerified")
                    is_Paid =dictionary.get("isPaid")
                    agent_amount = dictionary.get("Agent_charge")
                    if is_verified:
                        Total_Verified= Total_Verified+1
                    if is_Paid:
                        Total_paid= Total_paid+1
                        Totl_Paid_amount=Totl_Paid_amount+agent_amount
                    if not is_Paid:
              
                        Totl_UnPaid_amount=Totl_UnPaid_amount+agent_amount

                    if is_verified==True and is_Paid==True:
                        Total_Ver_Paid_amount = Total_Ver_Paid_amount+agent_amount

                    if is_verified==True and is_Paid==False:
                        Total_Ver_Unpaid_amount = Total_Ver_Unpaid_amount+agent_amount
                    
            
            
               
        Total_unVer_Paid_amount=Total_paid-Total_Ver_Paid_amount
       
        Payment_dict = {"Total_Verified": Total_Verified, 
                    "Total_paid": Total_paid, "Totl_Paid_amount": Totl_Paid_amount,
                     "Total_Ver_Paid_amount": Total_Ver_Paid_amount,
                     "Total_Ver_Unpaid_amount": Total_Ver_Unpaid_amount,
                     "Total_num": Total_num,
                     "Totl_UnPaid_amount": Totl_UnPaid_amount,
                     }
        list_payment=[]
        list_payment.append(Payment_dict)

    
        if list_dict==[]:
            messages.info(request,name+' not added anything on this date range')
            html_template = loader.get_template( 'transactions.html' )
            return HttpResponse(html_template.render({'context0':Data_list}, request)) 

        html_template = loader.get_template( 'transactions.html' )
        return HttpResponse(html_template.render({'context':list_dict,'context0':Data_list,'context1':list_payment}, request))   

    
    

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
