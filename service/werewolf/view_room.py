# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.core.context_processors import csrf
from django import forms
from models import Chat

def room(request):
    username = request.user.username
    roomnum = request.GET.get('roomnum')
    if roomnum is None:
        roomnum = '无'
    return render(request, "room.html", locals())

def chat(request):
    username = request.user.username
    chats = Chat.objects.filter(id__gt = 0)
    return render(request, "chat.html", locals())