from django.shortcuts import render, redirect
from django.urls import reverse
from home.SQLInjectionCheck import isValid
from django.http import HttpResponseRedirect

# Middleware for SQL Injection checking
class SQLInjectionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        self.process_request(request)
        return self.get_response(request)   

    def process_request(self, request):
        post_data = request.POST.dict()
        
        print(post_data)

        errors = False

        if post_data is not None:
            for data in post_data.values():
                if isValid(data) is False:
                    pass
                else:
                    errors = True
                    break
        
        if errors:
            request.injection = True
        else:
            request.injection = False

        print(request.injection)
