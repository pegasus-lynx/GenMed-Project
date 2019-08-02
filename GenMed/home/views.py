from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
import MySQLdb

#this file includes function for sql queries used by multiple views.
from GenMed.mysql import *

def is_valid_email(email):
    return True

# View for displaying the homepage in the home app
def home(request):
    context = {}
    return render(request, 'home/home.html', context)

def sqlerror(request):
    return render(request, 'home/sqlerror.html', context = {})

# View for logging in 
def logIn(request):
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    db=connect()
    c=db.cursor()
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print('1.',str(user))
            return redirect(reverse('shop:dashboard'))
        else:    
            context = { 'error':True }
            return render(request, 'home/loginpage.html', context)
    else:
        get_userlist(request,c)
        context = { 'error':False }
        return render(request, 'home/loginpage.html', context)

# View for logging out
def logOut(request):
    try:
        logout(request)
    except ValueError:
        pass
    return redirect(reverse('home:home'))

# View for registering
def register(request):
    db=connection
    c=db.cursor()
    userlist = get_userlist(request,c)
    if request.method=='POST':
        q = request.POST.dict()
        print(q)
        if q['password'] != q['cnf_password']:
            err = "Passwords don't match"
            return render(request, 'home/register.html', context= { 'err': err })
        elif not is_valid_email(q['email']):
            err = "Invalid email"
            return render(request, 'home/register.html', context= { 'err': err })
        elif q['username'] in userlist:
            err = "Username already taken"
            return render(request, 'home/register.html', context= { 'err': err })
        else:
            c.execute(
                """ INSERT into shop(username,email,passwd) 
                    values (%s,%s,%s) """,
                    (q['username'],q['email'],q['password'])
            )
            db.commit()
            p = User(username=q['username'],password=q['password'])
            p.save()
            login(request,p)
            return render(request, 'home/createshop.html', context = {})
    else:
        context = { 'userlist':userlist }
        return render(request, 'home/register.html', context)

# View for creating a shop object
@login_required
def createshop(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    if request.user.is_authenticated:
        if request.method == 'POST':
            q = request.POST.dict()
            shop_id = get_max_shopid(request,c)+1
            user_id = get_userid_by_name(request,c)
            
            # insert into shop_info
            c.execute(
                """ INSERT into shop_info(shop_id,name,owner_name,
                    mob_no,alt_no,license,user_id) values(%s,%s,%s,%s,%s,%s,%s) """,
                    (shop_id,q['shop_name'],q['owner_name'],
                        q['mob_no'],q['alt_no'],q['license'],user_id)
            )
            db.commit()
            
            # insert into the pharmacist table the pharmacist details
            c.execute(
                """ INSERT into ph_detail(name,deg,college)
                    values(%s,%s,%s) """,
                    (q['ph_name'],q['ph_deg'],q['ph_college'])
            )
            db.commit()

            # get the ph_id of the saved pharmacist
            c.execute(
                """ SELECT ph_id
                    from ph_detail
                    where name = %s and deg = %s and college = %s """,
                    (q['ph_name'],q['ph_deg'],q['ph_college'])
            )
            
            ph_id=str(c.fetchone()[0])
            
            # inserts information in the shop_license table
            c.execute(
                """ INSERT into shop_license(shop_id,ph_id,license,dr_license_type,dr_license_no)
                    values(%s,%s,%s,%s,%s) """,
                    (shop_id,ph_id,q['license'],q['drug_license_type'],q['drug_license'])
            )
            db.commit()

            # insert into the shop_location table
            c.execute(
                """ INSERT into shop_loc(shop_id,lat,lon,
                    state,district,city) values(%s,%s,%s,%s,%s,%s) """,
                    (shop_id,q['lat'],q['lon'],
                     q['state'],q['district'],q['city'])
            )
            db.commit()
            return redirect(reverse('shop:dashboard'))
        else:
            context = {}
            return render(request, 'home/createshop.html', context)
    else:
        context = {}
        return render(request, 'home/createshop.html', context)