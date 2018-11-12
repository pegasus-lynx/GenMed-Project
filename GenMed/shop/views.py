from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import MySQLdb

def shopheader(request):
    return render(request, 'shop/shop_header.html', context = {})

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

def get_shopid(request,c):
    username = request.user.username
    print('-'*100)
    print(username)
    c.execute(
        """ select shop_id from shop
            where username = %s """ ,
            (username,)
    )
    return c.fetchone()

def get_userinfo(request,c,shop_id):
    c.execute(
        """ select username,first_name,last_name,email
            from shop where shop_id = %s """,
            (shop_id,)
    )
    keys = [ 'username','first_name','last_name','email']
    res = c.fetchone()
    user_info = {}
    for i in range(len(keys)):
        user_info[keys[i]]=res[i]
    return user_info

def get_license(request,c,shop_id):
    c.execute(
        """ select SL.license,SL.dr_license_no,PD.ph_id,PD.name,PD.deg,PD.college
            from shop_license as SL inner join ph_detail as PD on 
            PD.ph_id = SL.ph_id
            where SL.shop_id = %s """,
            (shop_id,)
    )
    keys = [ "license", "drug_license", "ph_id","ph_name","deg","college"]
    res = c.fetchone()
    shop_license = {}
    for i in range(len(keys)):
        shop_license[keys[i]]=res[i]
    
    return shop_license

def get_curstock(request,c,shop_id):
    c.execute(
        """ select med_info.gen_name,avail.units,avail.price,avail.mfg_date,avail.exp_date,avail.batch
            from med_info,avail
            where avail.shop_id = %s and med_info.med_id=avail.med_id""",
            (shop_id,)
    )

    # keys = ['med_id', 'gen_name', 'units', 'price', 'mfg_date', 'exp_date', 'batch']
    res = map(list,c.fetchall())

    cur_stock = {}
    for i in res:
        cur_stock[i[0]]=i[1:]

    return cur_stock

#dashboard done
def dashboard(request):   
    if request.user.is_authenticated:
        db=connect()
        c=db.cursor()
        shop_id = get_shopid(request,c)[0]

        print(shop_id)
        # user_info = get_userinfo(request,c,shop_id)
        c.execute(
            """ select name,owner_name,mob_no,alt_no 
                from shop_info where shop_id = %s""",
                (shop_id,)
        )

        keys = ["shop_name","owner_name","mob_no","alt_no"]
        res = c.fetchone();

        shop_info = {}
        for i in range(len(keys)):
            shop_info[keys[i]]=res[i]
        
        c.execute(
            """ select city,district,state
                from shop_loc where shop_id = %s """,
                (shop_id,)
        )
        keys = ["city","district","state"]
        res = c.fetchone();

        shop_loc = {}
        for i in range(len(keys)):
            shop_loc[keys[i]]=res[i]

        print('shop_id',shop_id)
        print('shop_loc',shop_loc)
        print('shop_info',shop_info)

        context = {'shop_id':shop_id , 'shop_loc':shop_loc, 'shop_info':shop_info}
        return render(request, 'shop/dashboard.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)    

#profile done
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

#template done for curstock       
@login_required
def cur_stock(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        
        db=connect()
        c=db.cursor()
        
        shop_id = get_shopid(request,c)
        cur_stock = get_curstock(request,c,shop_id)
        #preprocess the dates to paas as a string to the template
        print(cur_stock)
        context = { 'shop_id':shop_id, 'cur_stock':cur_stock }
        return render(request, 'shop/curstock.html', context)

    else:
        context = {}
        return render(request, 'home/login-page.html', context)

#license done
@login_required
def license(request):
    if request.user.is_authenticated():
        
        db=connect()
        c=db.cursor()
        
        shop_id = get_shopid(request,c)
        #user_info = get_userinfo(request,c)
        shop_license = get_license(request,c,shop_id)
        
        print(shop_license)

        context = {'shop_id':shop_id , 'shop_license':shop_license }
        return render(request, 'shop/license.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)
            
@login_required
def update_info(request):
    db=connect()
    c=db.cursor()
    # Updates shop location, shop basic info ....

    if request.user.is_authenticated():
        if request.method == 'POST':
            q = request.POST.dict()
            
            shop_id = get_shopid(request,c)
            #user_info = get_userinfo(request,c)
            cur_shop_info = get_shopinfo(request,c)

            update = False
            keys = ["shop-name","owner_name","mob_no","alt_no"]

            for i in keys:
                if cur_shop_info[i] != q[i]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_info
                        set name = %s, owner_name = %s, mob_no= %s,  alt_no= %s
                        where shop_id = %s """,
                        (*[ q[i] for i in keys ],shop_id,) 
                )

            update = False
            keys = ["street","city","district","state"]

            for i in keys:
                if cur_shop_info[i] != q[i]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_loc
                        set street = %s, city = %s, district = %s,  state= %s
                        where shop_id = %s """,
                        (*[ q[i] for i in keys ],shop_id,) 
                )

                if q['change_cord']:
                    return redirect(reverse('update-cord'))
                else:
                    return redirect(reverse('dashboard'))

        else:
            context = {}
            return render(request, 'shop/update/info.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def update_license(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        if request.method == 'POST':
            q = request.POST.dict()
            cur_shop_license = get_license(request,c,shop_id)
        
            update = False
            keys = [ "license", "drug-license" ,"ph-name","deg","college"]
            
            for i in keys[:2]:
                if cur_shop_license[i] != q[i]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_license
                        set license = %s, dr_license_no = %s
                        where shop_id = %s """,
                        (q['license'],q['dr_license_no'],shop_id,) 
                )
            
            update = False
            for i in keys[2:]:
                if cur_shop_license[i] != q[i]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update ph_detail
                        set ph_name = %s, deg = %s, college = %s
                        where shop_id = %s """,
                        (q['ph_name'],q['deg'],q['college'],shop_id,) 
                )

            return redirect(reverse('dashboard'))
        else:
            shop_license = get_license(request,c,shop_id)
            heads = ["license", "drug_license", "ph_id","ph_name","deg","college"]
            context = {'shop_id':shop_id , 'shop_license':shop_license }
            return render(request, 'shop/update/license.html', context)


@login_required
def update_stock(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        if request.method == 'POST':
            return redirect(reverse('shop:cur_stock'))
        else:
            cur_stock = get_curstock(request,c,shop_id)
            heads = [ 'gen_name', 'units', 'price', 'mfg_date', 'exp_date', 'batch']
            context = { 'shop_id':shop_id, 'cur_stock':cur_stock , 'heads':heads}
            return render(request, 'shop/updatestock.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def update_med(request):
    db=connect()
    c=db.cursor()
    med_id = request.GET.get('med_id')

    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        if request.method == 'POST':
            q= request.POST.dict()
            keys = [ 'med_id', 'units', 'price', 'mfg_date', 'exp_date', 'batch']

            c.execute(
                """ update avail 
                    set units = %s, price = %s, mfg_date = %s, exp_date = %s, batch = %s
                    where med_id = %s and shop_id = %s """ ,
                    (q['units'],q['price'],q['mfg_date'],q['exp_date'],q['batch'],q['med_id'],shop_id)
            )

            db.commit()
            return redirect(reverse('shop:update_stock'))
        else:
            c.execute(
                """ select gen_name from med_info
                    where med_id = %s """,
                    (med_id,)
            )
            gen_name = c.fetchone()[0]
            print(gen_name)
            c.execute(
                """ select units,price,mfg_date,exp_date,batch from avail
                    where med_id = %s and shop_id = %s """ ,
                    (med_id,shop_id,)
            )

            med_details = list(c.fetchone())
            print(med_details)

            context = { 'gen_name':gen_name, 'med_details':med_details }
            return render(request,'shop/updatemed.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def add_med(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        if request.method == 'POST':
            q= request.POST.dict()
            keys = [ 'gen_name', 'units', 'price', 'mfg_date','exp_date', 'batch']
            
            med_id = get_medid(request,c,q['gen_name'])

            if med_id is None:
                c.execute(
                    """ insert into med_info values (%s) """,
                    (q['gen_name'],)
                )
                db.commit()

            med_id = get_medid(request,c,q['gen_name'])

            c.execute(
                """ insert into avail(med_id,shop_id,units,price,mfg_date,exp_date,batch) 
                    values (%s,%s,%s,%s,%s,%s,%s)""" ,
                    (med_id,shop_id,q['units'],q['price'],q['mfg_date'],q['exp_date'],q['batch'])
            )

            db.commit()
            return redirect(reverse('shop:update_stock'))
        else:
            context = {}
            return render(request,'shop/addmed.html',context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

@login_required
def update_cord(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated():
        if request.method == 'POST':
            q = request.POST.dict()
        
            shop_id = get_shopid(request,c)
            #user_info = get_userinfo(request,c)

            c.execute(
                """ update shop_loc
                    set lat = %s, lon = %s
                    where shop_id = %s """,
                    (q['lat'],q['lon'],shop_id,)
            )

            return redirect(reverse('dashboard'))
        else:
            context = {}
            return render(request, 'shop/update/cord.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)