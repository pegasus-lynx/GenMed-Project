from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import MySQLdb

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="bank")

# Create your views here.

def home(request):
    context = {}
    return render(request, 'home/homepage.html', context)

def logIn(request):
    db=connect()
    c=db.cursor()
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print(str(user))
            return redirect(reverse('shop-profile'))
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

def register(request):
    if request.method=='POST':
        print("POST")
        db=connect()
        c=db.cursor()

        # extract field information
        data = request.POST.dict()

        c.execute(
            """ INSERT into shop(username,email,password) 
                values (%s,%s,%s) """,
                (data['username'],data['email'],data['password'])
        )

        c.execute(
            """ SELECT shop_id 
                from shop
                where username=%s and email=%s """ ,
                (data['username'],data['email'])
        )
        
        data['shop_id']=str(c.fetchall())

        c.execute(
            """ INSERT into shop_info(shop_id,name,owner_name,
                mob_no,alt_no,license) values(%s,%s,%s,%s,%s,%s) """,
                (data['shop_id'],data['name'],data['owner_name'],
                data['mob_no'],data['alt_no'],data['license'])
        )
        
        c.execute(
            """ INSERT into ph_detail(name,deg,college)
                values(%s,%s,%s) """,
                (data['ph_name'],data['ph_deg'],data['ph_college'])
        )

        c.execute(
            """ SELECT ph_id
                from ph_detail
                where shop_id=%s """,
                (data['shop_id'])
        )
        
        data['ph_id']=str(c.fetchall())
        
        c.execute(
            """ INSERT into shop_loc(shop_id,lat,lon,
            state,district,city) values(%s,%s,%s,%s,%s,%s) """,
            (data['shop_id'],data['lat'],data['lon'],
            data['state'],data['district'],data['city'])
        )
        
        #return HttpResponse(request.POST.dict())
        return redirect(reverse('update-stock'))
    else:
        context = {}
        return render(request, 'home/signup-page.html', context)

