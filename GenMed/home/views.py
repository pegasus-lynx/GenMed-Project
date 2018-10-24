from django.shortcuts import render
from django.http import HttpResponse
import MySQLdb

def connect():
    return MySQLdb.connect(user="root",passwd="DKumar@14",db="bank")

# Create your views here.

def home(request):
    context = {}
    return render(request, 'home/homepage.html', context)

def login(request):
    if request.method=='POST':
        db=connect()
        c=db.cursor()
        c.execute(
            """ SELECT * from """,
            ()
        )

        
        return HtteResponse("Added!")
    else:
        context = {}
        return render(request, 'home/login-page.html', context)

def signup(request):
    if request.method=='POST':
        db=connect()
        c=db.cursor()
        # extract field information
        c.execute(
            """ INSERT into """,
            ()
        )
        c.execute(
            """ INSERT into """,
            ()
        )
        c.execute(
            """ INSERT into """,
            ()
        )
        db.commit()
        return HtteResponse("Added!")
    else:
        context = {}
        return render(request, 'home/signup-page.html', context)

