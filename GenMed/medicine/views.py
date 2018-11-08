from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import MySQLdb

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

def home(request):
    context = {}
    return render(request, 'medicine/home.html', context)

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

        # print(med_id)
        if med_id  is None:
            context = { "get_query":get_query }
        else:
            c.execute(
                """ SELECT gen_name from med_info where
                    med_id = %s """,
                    (med_id,)
            )
            gen_name= str(c.fetchall())

            c.execute(
                """ select custom_name, company_name from com_name
                    where med_id = %s """,
                    (med_id,)
            )
            common_name = list(c.fetchall())
            context = { 'get_query':get_query, 'gen_name':gen_name, 'common_name':common_name, }

    else:
        context = { 'get_query':False, }

    return render(request, 'medicine/info.html', context)

def query_medavail(request):
    db=connect()
    c=db.cursor()
    q=db.cursor()
    if request.method=='GET':
        med = request.GET.get('med-name')
        c.execute(
            """ SELECT med_id from com_name where
                custom_name = %s """,
                (med,)
        )
        med_id = c.fetchone()
        # print(med_id)
        if med_id is None:
            c.execute(
            """ SELECT med_id from med_info where
                gen_name = %s """,
                (med,)
            )
            med_id = c.fetchone()

        if med_id is None:
            context = { "get_query":True, 'gen_name':False }
        else:

            c.execute(
                """ select avail.shop_id,shop_info.name,avail.units,avail.price
                    from avail inner join shop_info on avail.shop_id=shop_info.shop_id
                    where avail.med_id = %s """,
                    (med_id,)
            )
            res = list(c.fetchall())
            shop_ids = [ i[0] for i in res ]
            shops = {}

            for i in range(len(shop_ids)):
                shops[res[i][0]] = res[i][1:]

            print(shop_ids)
            
            loc = {}
            for i in shop_ids:
                q.execute(
                    """ select lat, lon from shop_loc
                        where shop_id = %s """,
                        (i,)
                )
                cord = q.fetchone()
                loc[i] = cord

            context = {'get_query':True, 'med_id':med_id, 'loc':loc, 'shops':shops}
    else:
        context = { "get_query":False }
    return render(request, 'medicine/avail.html', context)
