from django.shortcuts import render,render_to_response

from django.http import HttpResponse,HttpResponseRedirect


def Home(request):
    return render(request, "game.html")
