from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from GenMed.mysql import *
import MySQLdb

# View for displaying the homepage of the medicine app
def home(request):
    context = {}
    return render(request, 'medicine/home.html', context)

# Displays the medicine information of the searched medicine
def query_medinfo(request):
    db=connect()
    c=db.cursor()
    context = {}
    get_query = 0
    if request.method=="GET":
        get_query = 1
        med = request.GET.get('med-name')
        c.execute(
            """ SELECT med_id from com_name where
                custom_name = %s """,
                (med,)
        )
        med_id = c.fetchone()
        if med_id  is None:
            context = { "get_query":get_query }
        else:
            c.execute(
                """ SELECT gen_name from med_info where
                    med_id = %s """,
                    (med_id,)
            )
            gen_name= c.fetchone()

            c.execute(
                """ select custom_name, company_name from com_name
                    where med_id = %s """,
                    (med_id,)
            )
            common_name = list(c.fetchall())
            context = { 'get_query':get_query, 'gen_name':gen_name[0], 'common_name':common_name, }
    elif request.method == 'POST':
        q = request.POST.dict()
        med_id = get_medid(request,c,q['gen_name'])

        # inserts the common name to the com_name
        c.execute(
            """ insert into com_name(med_id,company_name,custom_name) 
                values(%s,%s,%s)""" ,
                (med_id,q['company_name'],q['custom_name'])
        )
        db.commit()

        # selects the custom names of the drug using the med_id
        c.execute(
            """ select custom_name, company_name from com_name
                where med_id = %s """,
                (med_id,)
        )
        common_name = list(c.fetchall()) 
        context = { 'get_query':1, 'gen_name':q['gen_name'], 'common_name':common_name, }
        return render(request, 'medicine/info.html', context)
    else:
        context = { 'get_query':False, }

    return render(request, 'medicine/info.html', context)

# Displays the information about the medicine that where it is available
def query_medavail(request):
    db=connect()
    c=db.cursor()
    q=db.cursor()
    if request.method=='GET':
        med = request.GET.get('med-name')
        if med is not None:
            med_id = get_med(request,c,med)
        else:
            med_id = None
        if med_id is None and med is None:
            context = { "get_query":False}
        elif med_id is None:
            context = { "get_query":True, 'name':med }
        else:
            med_id = med_id[0]
            shops = get_shops_by_med(request,c,med_id)
            shop_ids = list(shops.keys())
            loc = {}
            for i in shop_ids:
                loc[i]=get_shopcord(c,i)
                loc[i]+=get_city(c,i)

                
            print(loc[i])
            context = {'get_query':True, 'med_id':med_id, 'shops':shops, 'loc':loc}
    else:
        context = { "get_query":False }
    return render(request, 'medicine/avail.html', context)