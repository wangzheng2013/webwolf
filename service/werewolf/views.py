from django.shortcuts import render,render_to_response

from django.http import HttpResponse,HttpResponseRedirect


def Home(request):
    return render(request, "home.html")

def signin(request):
    return render(request, "home.html")

def room(request):
    return render(request, "room.html")
