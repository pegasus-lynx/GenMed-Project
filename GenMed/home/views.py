from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
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

        print(request.POST.dict())

        # c.execute(
        #     """ INSERT into """,
        #     ()
        # )
        # c.execute(
        #     """ INSERT into """,
        #     ()
        # )
        # c.execute(
        #     """ INSERT into """,
        #     ()
        # )
        # db.commit()
        return redirect(reverse('shop-profile'))
    else:
        context = {}
        return render(request, 'home/signup-page.html', context)

