from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import MySQLdb

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

@login_required
def dashboard(request):    
    if request.user.is_authenticated():
        db=connect()
        c=db.cursor()
        username = request.user.username
        c.execute(
            """ select shop_id from shop
                where username = %s """ ,
                (username,)
        )

        shop_id = c.fetchone()

        c.execute(
            """ select name,owner_name,mob_no,alt_no 
                from shop_info where shop_id = %s""",
                (shop_id,)
        )
        keys = ["shop-name","owner_name","mob_no","alt_no"]
        res = c.fetchone();

        shop_info = {}
        for i in range(len(keys)):
            shop_info[keys[i]]=res[i]
        
        c.execute(
            """ select street,city,district,state
                from shop_loc where shop_id = %s """,
                (shop_id,)
        )
        keys = ["street","city","district","state"]
        res = c.fetchone();

        shop_loc = {}
        for i in range(len(keys)):
            shop_loc[keys[i]]=res[i]

        c.execute(
            """ select SL.license,SL.dr_license_no,PD.ph_id,PD.name,PD.deg,PD.college
                from shop_license as SL inner join ph_detail as PD on 
                PD.ph_id = SL.ph_id
                where SL.shop_id = %s """,
                (shop_id,)
        )
        keys = [ "license", "drug-license", "ph-id","ph-name","deg","college"]
        res = c.fetchone()

        shop_license = {}
        for i in range(len(keys)):
            shop_license[keys[i]]=res[i]

        context = {'shop_id':shop_id , 'shop_license':shop_license, 'shop_loc':shop_loc, 'shop_info':shop_info}
        return render(request, 'shop/dashboard.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def update_stock(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated():
        if request.method == 'POST':

        else:
            context = {}
            return render(request, 'shop/profile.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)    

def profile(request):
    db=connect()
    c=db.cursor()
    if request.method=="GET":
        get_query = 1
        shop_name = request.GET.get('shop-name')

        c.execute(
            """ select shop_id from shop
                where name = %s """,
                (shop_name,)
        )
        shop_id = c.fetchone()
        
        # if results = "":
        #     context = { 'found' = "null", 'shop_name' = shop_name}
        # else:
        if shop_id is None:
            context = { 'found':None, 'shop_name':shop_name , 'type':'shop'}
            return render(request, 'home/notfound.html', context)
        else:
            c.execute(
                """ select name,owner_name,mob_no,alt_no 
                    from shop_info where shop_id = %s""",
                    (shop_id,)
            )
            keys = ["shop-name","owner_name","mob_no","alt_no"]
            res = c.fetchone();

            shop_info = {}
            for i in range(len(keys)):
                shop_info[keys[i]]=res[i]
            
            c.execute(
                """ select street,city,district,state
                    from shop_loc where shop_id = %s """,
                    (shop_id,)
            )
            keys = ["street","city","district","state"]
            res = c.fetchone();

            shop_loc = {}
            for i in range(len(keys)):
                shop_loc[keys[i]]=res[i]

            c.execute(
                    """ select lat, lon from shop_loc
                        where shop_id = %s """,
                        (shop_id,)
                )
                
            cord = q.fetchone()
            context = { 'shop_info':shop_info, 'shop_loc':shop_loc, 'cord':cord}
    else:
        get_query = 0
        context = { 'get_query':get_query, }
    return render(request, 'medicine/info.html', context)

@login_required
def cur_stock(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated():
        db=connect()
        c=db.cursor()
        username = request.user.username
        c.execute(
            """ select shop_id from shop
                where username = %s """ ,
                (username,)
        )
        shop_id = c.fetchone()

        c.execute(
            """ select med_info.gen_name,avail.units,avail.price,avail.batch,avail.exp_date
                from med_info outer join avail using (med_id)
                where shop_id = %s """,
                (shop_id,)
        )

        cur_stocks = list(c.fetchall())

        context = { 'shop_id':shop_id, 'cur_stock':cur_stock }
        return render(request, 'shop/curstock.html', context)

    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def update_profile(request):
