from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Comment
from GenMed.mysql import *
import MySQLdb

def getCenter(shops):
    center = { 'lat':0, 'lon':0 }
    if len(shops)==0:
        return center
    for shop in shops:
        center['lat'] += shop['lat']
        center['lon'] += shop['lon']

    center['lat'] /= len(shops)
    center['lon'] /= len(shops)
    return center

# Displays the homepage in the shop
def home(request):
    return render(request, 'shop/home.html', context = {})

# Displays the dashboard to the shop_owners from where they can access any records
def dashboard(request):   
    if request.user.is_authenticated:
        db=connect()
        c=db.cursor()

        shop_id = get_shopid(request,c)
        shop_info = get_shopinfo(request,c,shop_id)
        shop_loc = get_shoploc(request,c,shop_id)

        print('shop_id',shop_id)
        print('shop_loc',shop_loc)
        print('shop_info',shop_info)

        context = {'shop_id':shop_id , 'shop_loc':shop_loc, 'shop_info':shop_info}
        return render(request, 'shop/dashboard.html', context)
    else:
        context = {}
        return render(request, 'home/loginpage.html', context)    

# displays the profile page to the consumers including their owner, contact detail and address
def profile(request,shop_id):
    db=connect()
    c=db.cursor()

    shop_ids = get_shopid_list(c)

    if shop_id in shop_ids:
        shop_info = get_shopinfo(request,c,shop_id)
        shop_loc = get_shoploc(request,c,shop_id)
        shop_cord = get_shopcord(c,shop_id)

        context = { 'shop_info':shop_info, 'shop_loc':shop_loc, 'shop_cord':shop_cord}
        return render(request, 'shop/profile.html', context)
    else:
        context={}
        return render(request, 'shop/profile.html', context)

# Displays the information for the current stocks in the shop     
@login_required
def cur_stock(request):
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        
        db=connect()
        c=db.cursor()
        
        shop_id = get_shopid(request,c)
        cur_stock = get_curstock(request,c,shop_id)
        print(cur_stock)
        context = { 'shop_id':shop_id, 'cur_stock':cur_stock }
        return render(request, 'shop/curstock.html', context)

    else:
        context = {}
        return render(request, 'home/loginpage.html', context)

# Displays the license information of the shop
@login_required
def license(request):
    # print(request.injection)
    if request.user.is_authenticated:
        
        db=connect()
        c=db.cursor()
        
        shop_id = get_shopid(request,c)
        shop_license = get_license(request,c,shop_id)
        
        print(shop_license)

        context = {'shop_id':shop_id , 'shop_license':shop_license }
        return render(request, 'shop/license.html', context)
    else:
        context = {}
        return render(request, 'home/loginpage.html', context)

# View for updating the information of the the shop      
@login_required
def update_info(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        cur_shop_info = get_shopinfo(request,c,shop_id)
        cur_shop_loc = get_shoploc(request,c,shop_id)
        if request.method == 'POST':
            q = request.POST.dict()

            update = False
            keys = ["shop_name","owner_name","mob_no","alt_no"]

            for i in range(len(keys)):
                if cur_shop_info[i][1] != q[cur_shop_loc[i][0]]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_info
                        set name = %s, owner_name = %s, mob_no= %s,  alt_no= %s
                        where shop_id = %s """,
                        (*[ q[i] for i in keys ],shop_id,) 
                )
                db.commit()

            update = False
            keys = ["city","district","state"]

            for i in range(len(keys)):
                if cur_shop_info[i][1] != q[cur_shop_loc[i][0]]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_loc
                        set city = %s, district = %s,  state= %s
                        where shop_id = %s """,
                        (*[ q[i] for i in keys ],shop_id,) 
                )
                db.commit()
            
            return redirect(reverse('shop:dashboard'))
                # if q['change_cord']:
                #     return redirect(reverse('update_cord'))
                # else:
                #     return redirect(reverse('dashboard'))

        else:
            context = { 'shop_id':shop_id, 'shop_info':cur_shop_info, 'shop_loc':cur_shop_loc }
            return render(request, 'shop/updateinfo.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

# View used for upddating the license information
# of the shop data.
@login_required
def update_license(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        cur_shop_license = get_license(request,c,shop_id)
        if request.method == 'POST':
            q = request.POST.dict()
            print(q)       
            update = False
            keys = [ "license", "drug-license", "ph_id" ,"ph_name","deg","college"]
            
            for i in range(0,2):
                if cur_shop_license[i] != q[keys[i]]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update shop_license
                        set license = %s, dr_license_no = %s
                        where shop_id = %s """,
                        (q['license'],q['drug_license'],shop_id,) 
                )
                db.commit()
            
            update = False
            for i in range(3,5):
                if cur_shop_license[i] != q[keys[i]]:
                    update = True
                    break

            if update:
                c.execute(
                    """ update ph_detail
                        set name = %s, deg = %s, college = %s
                        where ph_id = %s """,
                        (q['ph_name'],q['deg'],q['college'],q['ph_id'],) 
                )
                db.commit()

            return redirect(reverse('shop:dashboard'))
        else:
            context = {'shop_id':shop_id , 'shop_license':cur_shop_license }
            return render(request, 'shop/updatelicense.html', context)

# Main page for updating the stock page of the shop
@login_required
def update_stock(request):
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    db=connect()
    c=db.cursor()
    if request.user.is_authenticated:
        q = request.POST.dict()
        shop_id = get_shopid(request,c)
        if request.method == 'POST':
            if q['submit'] == 'Update':
                return redirect(reverse('shop:cur_stock'))
            else:
                return redirect(reverse('shop:add_med'))
        else:
            cur_stock = get_curstock(request,c,shop_id)
            med_ids = list(cur_stock.keys())
            med_ids.sort()

            heads = [ 'gen_name', 'units', 'price', 'mfg_date', 'exp_date', 'batch']
            context = { 'shop_id':shop_id, 'cur_stock': cur_stock , 'heads':heads, 'med_ids':med_ids}
            return render(request, 'shop/updatestock.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

# View for updating the stock details like the price, units ,
# mfg_date and exp_date of the medicine in stock of the shop.
@login_required
def update_med(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    med_id = request.GET.get('med_id')

    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        keys = [ 'med_id', 'units', 'price','batch', 'mfg_date', 'exp_date']
        if request.method == 'POST':
            q= request.POST.dict()
            
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
                """ select med_id,units,price,batch,mfg_date,exp_date from avail
                    where med_id = %s and shop_id = %s """ ,
                    (med_id,shop_id,)
            )

            res = list(c.fetchone())
            med_details = []
            for i in range(len(keys)):
                med_details.append([keys[i],res[i]])

            med_details[4][1]=str(med_details[4][1])
            med_details[5][1]=str(med_details[5][1])
            print(med_details)

            context = { 'gen_name':gen_name, 'med_details':med_details }
            return render(request,'shop/updatemed.html', context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

# View for adding a generic medicine to the database 
@login_required
def add_med(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    if request.user.is_authenticated:
        shop_id = get_shopid(request,c)
        keys = [ 'gen_name', 'units', 'price', 'batch', 'mfg_date','exp_date']
        if request.method == 'POST':
            q = request.POST.dict() 
            med_id = get_medid(request,c,q['gen_name'])

            if med_id is None:
                c.execute(
                    """ insert into med_info(gen_name) values (%s) """,
                    (q['gen_name'],)
                )
                db.commit()

            med_id = get_medid(request,c,q['gen_name'])
            print(med_id)
            c.execute(
                """ insert into avail(med_id,shop_id,units,price,mfg_date,exp_date,batch) 
                    values (%s,%s,%s,%s,%s,%s,%s)""" ,
                    (med_id,shop_id,q['units'],q['price'],q['mfg_date'],q['exp_date'],q['batch'])
            )
            db.commit()
            return redirect(reverse('shop:update_stock'))
        else:
            context = { 'keys':keys, }
            return render(request,'shop/addmed.html',context)
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

# View for updating the coordinates of the shop
@login_required
def update_cord(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
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

def map(request):
    context = {}
    return render(request, 'shop/map.html', context)

# View for getting the shops by city or name
def search(request):
    db=connect()
    c=db.cursor()
    # if request.injection:
    #     return redirect(reverse('home:sqlerror'))
    if request.method == 'GET':
        param = request.GET.get('param')
        tag = request.GET.get('tag')
        if 'name' in tag.lower():
            shop_list = get_shopname_list(c)
            shops = {}
            for shop in shop_list:
                if param in shop:
                    shop_id = get_shopid_by_name(c,param)
                    if shop_id is not None:
                        res = get_shop_search(c,shop_id)
                        shops[shop_id]=res
        else:
            shops = get_shop_by_city(c,param)
        

        print(len(shops))
        context = {'get_query':True, 'shops':shops, 'center':getCenter(shops) }
        return render(request, 'shop/search.html', context)
    else:
        context = {'get_query': False}
        return render(request, 'shop/search.html', context)

# View for getting the feed related to the shop comment        
def feeds(request,comment_no):
    mycomment = Comment.objects.get(comment_no = comment_no)
    text = '<p><h1>Title : %s </h1></p>' % ( mycomment.title,)
    text += '<p><h3>Comment No. : %s </h3></p>' % ( mycomment.comment_no, )
    text += '<p><h3>Shop Name : %s</h3></p>' % (mycomment.shop_id, )
    text += '<p> Comment : <br> %s </p>' % ( mycomment.text, )
    return HttpResponse(text)

def comment(request):
    if request.method == 'POST':
        q = request.POST.dict()
        com = Comment(title=q['title'],shop_id=q['shop_id'],text=q['comment'])
        com.save()
        return redirect(reverse('shop:home'))       
    else:
        return render(request, 'shop/comment.html', context={})