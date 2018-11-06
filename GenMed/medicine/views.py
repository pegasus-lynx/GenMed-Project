from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import MySQLdb

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="bank")

def home(request):
    context = {}
    return render(request, 'medicine/home.html', context)

def query_medinfo(request):
    db=connect()
    c=db.cursor()
    get_query = 0
    if request.method=="GET":
        get_query = 1
        med = request.GET.get('med-name')
        c.execute(
            """ SELECT med_id from com_name where
                custom_name = %s """,
                (med,)
        )
        med_id = str(c.fetchall())

        if med_id is NULL:
            context = { "get_query":get_query, 'gen_name':"null" }
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
        get_query = 0
        context = { 'get_query':get_query, }

    return render(request, 'medicine/info.html', context)

def query_medavail(request):
    db=connect()
    c=db.cursor()
    if request.method=='GET':
        med = request.GET.get('med-name')
        c.execute(
            """ SELECT med_id from com_name where
                custom_name = %s """,
                (med,)
        )
        med_id = str(c.fetchall())

        if med_id is NULL:
            context = { "get_query":get_query, 'gen_name':"null" }
        else:
            

    else:
        context = {}
    return render(request, 'medicine/avail.html', context)
