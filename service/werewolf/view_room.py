# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.core.context_processors import csrf
from django import forms

def room(request):
    username = request.user.username
    roomnum = request.GET.get('roomnum')
    if roomnum is None:
        roomnum = '无'
    return render(request, "room.html", locals())