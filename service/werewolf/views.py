from django.shortcuts import render,render_to_response

from django.http import HttpResponse,HttpResponseRedirect
from models import User


def Home(request):
    return render(request, "home.html")

