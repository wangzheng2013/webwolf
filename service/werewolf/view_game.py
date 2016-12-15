# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from werewolf import *
from models import GameInfo, Game2User, SystemCommand

def wolf(gameId):
    """
    实际用户狼人操作经过一个晚上
    :param gameId:
    :return: None
    """

    return

@csrf_exempt
def get_system_command(request):
    if request.method == 'POST':
        last_chat_id = int(request.POST.get('last_chat_id'))
        chats = SystemCommand.objects.filter(id__gt = last_chat_id)
        return render(request, 'chat_list_item.html', {'chats': chats})
    else:
        raise Http404

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
    chats = SystemCommand.objects.filter(gameId = 1)
    wolf_move = False
    witch_move = False
    seer_move = False
    victim = game.getVictim()
    witchA = game.getWitchA()
    witchP = game.getWitchP()
    for chat in chats:
        system_command = eval(chat.content)
        if system_command['command'] == 'Werewolf':
            wolf_move = True
        if system_command['command'] == 'Witch':
            witch_move = True
        if system_command['command'] == 'Seer':
            seer_move = True
    return render(request, "game_api.html", locals())

def post_game(request):
    if request.method == 'POST':
        # 传递所有游戏需要的post信息的接口
        gameId = 1
        response = request.META.get('HTTP_REFERER', '/')
        command = request.POST.get('action')
        if command == u'创建游戏':
            # 删除上一局的信息
            Game2User.objects.filter(gameId = gameId).delete()
            # 新建一个游戏,并且保存到数据库中
            game = werewolf_game(str({}))
            characters = game.characterList()
            for (seat, character) in characters:
                user = Game2User()
                user.gameId = gameId
                user.character = int(character)
                user.user = request.user
                user.seat = seat
                user.save()
            # 在数据库中保存相应的游戏信息
            GameInfo.objects.filter(gameId = gameId).delete()
            gameInfo = GameInfo()
            gameInfo.gameId = gameId
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Werewolf'
            syscommand.content = str(tmp)
            syscommand.save()
        if command == u'白天':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            game.GoThroughDay()
            GameInfo.objects.filter(gameId = gameId).delete()
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        if command == u'黑夜':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            game.GoThroughNight()
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        if command == u'狼刀' or command == u'空刀':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            if command == u'狼刀':
                target = int(request.POST.get('target'))
                game.Wolf(target = target)
            else:
                game.Wolf(target = -1)
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Witch'
            syscommand.content = str(tmp)
            syscommand.save()
        if command == u'女巫救':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            game.witch(target = -1)
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Seer'
            syscommand.content = str(tmp)
            syscommand.save()
        if command == u'女巫毒':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            target = int(request.POST.get('target'))
            game.witch(target = target)
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Seer'
            syscommand.content = str(tmp)
            syscommand.save()
        if command == u'女巫过':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            game.witch(target = -2)
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Seer'
            syscommand.content = str(tmp)
            syscommand.save()
        if command == u'预言家':
            # 从数据库中拿出相应的游戏信息，处理后返回给数据库
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            target = int(request.POST.get('target'))
            game.seer(target = target)
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            tmp = {}
            tmp['command'] = 'Werewolf'
            syscommand.content = str(tmp)
            syscommand.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404
