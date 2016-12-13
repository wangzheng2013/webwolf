# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from werewolf import *
from models import GameInfo

def game_api(request):
    # 检查参数，正确则继续，错误则重定向到正确的参数
    seat = request.GET.get('seat')
    # 正式开始
    gameInfoList = GameInfo.objects.filter(gameId = 1)
    for info in gameInfoList:
        info.character = str(werewolf_character.CHARACTER(info.character))
    return render(request, "game_api.html", locals())

def post_game(request):
    if request.method == 'POST':
        # 传递所有游戏需要的post信息的接口
        response = request.META.get('HTTP_REFERER', '/')
        # 删除上一局的信息
        GameInfo.objects.filter(gameId = 1).delete()
        # 新建一个游戏,并且保存到数据库中
        game = werewolf_game()
        characters = game.characterList()
        for (seat, character) in characters:
            gameinfo = GameInfo()
            gameinfo.gameId = 1
            gameinfo.character = int(character)
            gameinfo.user = request.user
            gameinfo.seat = seat
            gameinfo.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404
