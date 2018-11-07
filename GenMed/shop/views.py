from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import MySQLdb

def connect():
    return MySQLdb.connect(user="django",passwd="djUser@123",db="GEN_MED")

def dashboard(request):


def update_stock(request):
    db=connect()
    c=db.cursor()
    if request.method == 'POST':

    else:
        context = {}
        return render(request, 'shop/profile.html', context)

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
        results = str(c.fetchall())
        print(results)
        if results = "":
            context = { 'found' = "null", 'shop_name' = shop_name}
        else:

    else:
        get_query = 0
        context = { 'get_query':get_query, }
    return render(request, 'medicine/info.html', context)

def cur_stock(request):


def update_profile(request):
