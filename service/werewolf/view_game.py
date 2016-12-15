# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from werewolf import *
from models import GameInfo, Game2User

def game_api(request):
    # 检查参数，正确则继续，错误则重定向到正确的参数
    seat = request.GET.get('seat')
    # 正式开始
    gameInfo = GameInfo.objects.filter(gameId = 1)
    if len(gameInfo) == 0:
        content = '{}'
    else:
        content = gameInfo[0].content
    game = werewolf_game(content)
    userList = Game2User.objects.filter(gameId = 1)
    for user in userList:
        user.character_name = str(werewolf_character(int(game.character[user.seat].character)).character)
        user.alive = game.character[user.seat].alive
    return render(request, "game_api.html", locals())

def post_game(request):
    if request.method == 'POST':
        # 传递所有游戏需要的post信息的接口
        response = request.META.get('HTTP_REFERER', '/')
        command = request.POST.get('action')
        if command == u'创建游戏':
            # 删除上一局的信息
            Game2User.objects.filter(gameId = 1).delete()
            # 新建一个游戏,并且保存到数据库中
            game = werewolf_game(str({}))
            characters = game.characterList()
            for (seat, character) in characters:
                user = Game2User()
                user.gameId = 1
                user.character = int(character)
                user.user = request.user
                user.seat = seat
                user.save()
            # 在数据库中保存相应的游戏信息
            GameInfo.objects.filter(gameId = 1).delete()
            gameInfo = GameInfo()
            gameInfo.gameId = 1
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        if command == u'白天':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = 1)[0]
            game = werewolf_game(gameInfo.content)
            game.GoThroughDay()
            GameInfo.objects.filter(gameId = 1).delete()
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        if command == u'黑夜':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = 1)[0]
            content = gameInfo.content
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = 1).delete()
            game.GoThroughNight()
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404
