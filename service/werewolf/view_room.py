# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from models import Chat, Game2User
from django.contrib.auth.models import User

def room(request):
    username = request.user.username
    roomnum = request.GET.get('roomnum')
    if roomnum is None:
        roomnum = 1
    chats = Chat.objects.filter(id__gt = 0)
    num = 12
    userList = []
    for i in range(num):
        userList.append(0)
    for i in range(num):
        tmp = Game2User.objects.filter(gameId = 1, seat = i)
        if len(tmp) == 1:
            userList[i] = tmp[0].user
        else:
            userList[i] = User()
            userList[i].username = 'NULL'
    return render(request, "room.html", locals())

def post_room(request):
    if request.method == 'POST':
        response = request.META.get('HTTP_REFERER', '/')
        seat = request.POST.get('seat')
        if seat is None:
            seat = 0
        gameId = request.POST.get('gameId')
        user = request.user
        Game2User.objects.filter(gameId = gameId, user = user).delete()
        tmp = Game2User()
        tmp.character = 0
        tmp.gameId = gameId
        tmp.seat = seat
        tmp.user = user
        tmp.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404

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

def post_chat(request):
    if request.method == 'POST':
        response = request.META.get('HTTP_REFERER', '/')
        chat = Chat()
        chat.content = request.POST.get('chat_content')
        chat.sender = request.user
        chat.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404