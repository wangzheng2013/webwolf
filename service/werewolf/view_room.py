# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django import forms
from models import Chat

def room(request):
    username = request.user.username
    roomnum = request.GET.get('roomnum')
    if roomnum is None:
        roomnum = '无'
    chats = Chat.objects.filter(id__gt = 0)
    return render(request, "room.html", locals())

def chat(request):
    username = request.user.username
    chats = Chat.objects.filter(id__gt = 0)
    return render(request, "chat.html", locals())

@csrf_exempt
def get_chat(request):
    if request.method == 'POST':
        last_chat_id = int(request.POST.get('last_chat_id'))
        chats = Chat.objects.filter(id__gt = last_chat_id)
        return render(request, 'chat_list_item.html', {'chats': chats})
    else:
        raise Http404