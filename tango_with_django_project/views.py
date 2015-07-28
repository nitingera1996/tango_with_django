from django.shortcuts import render
from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Welcome to my server <br/> Wanna check my latest application <a href = '/rango/'> Rango </a>")