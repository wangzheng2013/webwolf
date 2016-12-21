# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from werewolf import *
from models import GameInfo, Game2User, SystemCommand, userVote, Chat
from django.contrib.auth.decorators import login_required

@csrf_exempt
def get_system_command(request):
    if request.method == 'POST':
        last_chat_id = int(request.POST.get('last_chat_id'))
        chats = SystemCommand.objects.filter(id__gt = last_chat_id)
        return render(request, 'chat_list_item.html', {'chats': chats})
    else:
        raise Http404

def game_api(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signup/')
    # 检查参数，正确则继续，错误则重定向到正确的参数
    username = request.user.username
    seat = request.GET.get('seat')
    if seat is None:
        seat = -1
    else:
        seat = int(seat)
    gameId = 1
    visitor = False
    if Game2User.objects.filter(gameId = gameId, seat = seat, user = request.user).count() == 0:
        visitor = True

    # 正式开始
    gameInfo = GameInfo.objects.filter(gameId = gameId)
    if len(gameInfo) == 0:
        content = '{}'
    else:
        content = gameInfo[0].content
    game = werewolf_game(content)
    gameover = game.isFinished()  # 游戏是否结束
    num = game.getNum()
    userList = Game2User.objects.filter(gameId = gameId)
    for user in userList:
        user.character_name = str(werewolf_character(int(game.character[user.seat].character)).character)
        user.alive = game.character[user.seat].alive
        if visitor:
            if user.user == request.user:
                visitor = False
                seat = user.seat
    chats = SystemCommand.objects.filter(gameId = gameId)
    mchats = Chat.objects.filter(gameId = gameId)
    wolf_move = False
    witch_move = False
    seer_move = False
    vote_move = False
    police_move = False
    police_choose_move = False
    police_vote_move = False
    victim = game.getVictim()
    witchA = game.getWitchA()
    witchP = game.getWitchP()
    police = game.getPolice()
    allAliveState = game.getAllAliveState()
    idiotShow = game.findIdiot()   # 若白痴展现则为白痴座位号，否则为-1
    hunterGun = game.AbilityHunter() # True 表示猎人能开枪
    voters = []
    speaker = 0
    for chat in chats:
        system_command = eval(chat.content)
        if system_command['command'] == 'Witch':
            witch_move = True
        if system_command['command'] == 'Seer':
            seer_move = True
            deathLastNight = game.getAllDeath()
            for i in deathLastNight:
                allAliveState[i] = 1

        if system_command['command'] == 'PoliceSpeak' or system_command['command'] == 'Speak' or system_command['command'] == 'Last_words_Night' or system_command['command'] == 'Last_words_Day':
            # 状态 1 上警  2 退水  0 警下 [0~3] 还没覆盖过  [4~7]覆盖过
            speak_move = True
            speaker = system_command['speaker']
            if int(system_command['state'][speaker]) > 3:
                # 发言完毕 下一阶段
                tmp = system_command['state']
                if system_command['command'] == 'PoliceSpeak':
                    system_command = {}
                    system_command['command'] = 'PoliceVote'
                    system_command['state'] = tmp
                if system_command['command'] == 'Speak':
                    system_command = {}
                    system_command['command'] = 'Vote'
                    system_command['state'] = tmp
                if system_command['command'] == 'Last_words_Night':
                    system_command = {}
                    system_command['command'] = 'Day'
                if system_command['command'] == 'Last_words_Day':
                    system_command = {}
                    system_command['command'] = 'Werewolf'
                speak_move = False
                police_vote_move = True
            else:
                if system_command['clockwise'] == 0:
                    # 号数递增发言
                    if speaker >= game.getNum():
                        speaker = 0
                    while system_command['state'][speaker] != '1' and int(system_command['state'][speaker]) <= 3:
                        s = system_command['state']
                        system_command['state'] = ''
                        if speaker > 0:
                            system_command['state'] = system_command['state'] + s[0 : speaker]
                        system_command['state'] = system_command['state'] + str(int(s[speaker]) + 4)
                        if speaker < game.getNum() - 1:
                            system_command['state'] = system_command['state'] + s[speaker + 1 : game.getNum()]
                        speaker = speaker + 1
                        if speaker >= game.getNum():
                            speaker = 0
                        system_command['speaker'] = speaker
                    if int(system_command['state'][speaker]) > 3:
                        # 发言完毕 下一阶段
                        tmp = system_command['state']
                        if system_command['command'] == 'PoliceSpeak':
                            system_command = {}
                            system_command['command'] = 'PoliceVote'
                            system_command['state'] = tmp
                        if system_command['command'] == 'Speak':
                            system_command = {}
                            system_command['command'] = 'Vote'
                            system_command['state'] = tmp
                        if system_command['command'] == 'Last_words_Night':
                            system_command = {}
                            system_command['command'] = 'Day'
                        if system_command['command'] == 'Last_words_Day':
                            system_command = {}
                            system_command['command'] = 'Werewolf'
                        speak_move = False
                        police_vote_move = True
                else:
                    if speaker < 0:
                        speaker = game.getNum() - 1
                    while system_command['state'][speaker] != '1' and int(system_command['state'][speaker]) <= 3:
                        s = system_command['state']
                        system_command['state'] = ''
                        if speaker > 0:
                            system_command['state'] = system_command['state'] + s[0 : speaker]
                        system_command['state'] = system_command['state'] + str(int(s[speaker]) + 4)
                        if speaker < game.getNum() - 1:
                            system_command['state'] = system_command['state'] + s[speaker + 1 : game.getNum()]
                        speaker = speaker - 1
                        if speaker < 0:
                            speaker = game.getNum() - 1
                        system_command['speaker'] = speaker
                        if int(system_command['state'][speaker]) > 3:
                            # 发言完毕 下一阶段
                            tmp = system_command['state']
                            if system_command['command'] == 'PoliceSpeak':
                                system_command = {}
                                system_command['command'] = 'PoliceVote'
                                system_command['state'] = tmp
                            if system_command['command'] == 'Speak':
                                system_command = {}
                                system_command['command'] = 'Vote'
                                system_command['state'] = tmp
                            if system_command['command'] == 'Last_words_Night':
                                system_command = {}
                                system_command['command'] = 'Day'
                            if system_command['command'] == 'Last_words_Day':
                                system_command = {}
                                system_command['command'] = 'Werewolf'
                            speak_move = False
                            police_vote_move = True
            SystemCommand.objects.filter(gameId = gameId).delete()
            syscommand = SystemCommand()
            syscommand.gameId = gameId
            syscommand.content = str(system_command)
            syscommand.save()

        if system_command['command'] == 'Day':
            police_vote_move = False
            if police == -1:
                SystemCommand.objects.filter(gameId = gameId).delete()
                list = game.getAliveList()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Speak'
                tmp['state'] = ''
                for i in range(game.getNum()):
                    if i in list:
                        tmp['state'] = tmp['state'] + '1'
                    else:
                        tmp['state'] = tmp['state'] + '0'
                tmp['first'] = randint(0, game.getNum() - 1)
                tmp['clockwise'] = randint(0, 1)
                tmp['speaker'] = tmp['first']
                syscommand.content = str(tmp)
                syscommand.save()
                system_command = tmp
            else:
                police_choose_move = True

        if system_command['command'] == 'Werewolf':
            wolf_move = True
            police_vote_move = False

        day = 0
        voteList = []
        for i in range(game.getNum()):
            voteList.append(False)
        if system_command['command'] == 'Police':
            police_move = True
            day = 100
        if system_command['command'] == 'PoliceVote':
            police_vote_move = True
            day = 101
            for i in range(game.getNum()):
                if system_command['state'][i] != '4':
                    # 不在警下无法投票
                    voteList[i] = True
        if system_command['command'] == 'Vote':
            vote_move = True
            police_vote_move = False
            day = game.getDay()
            aliveList = game.getAliveList()
            for i in range(game.getNum()):
                if i not in aliveList:
                    voteList[i] = True
        votes = userVote.objects.filter(gameId = 1, day = day)
        for vote in votes:
            voteList[vote.seat] = True
        for i in range(game.getNum()):
            if voteList[i] == False:
                voters.append(i)
        if system_command.has_key('isWolf'):
            iswolf = system_command['isWolf']
        else:
            iswolf = -1
    votes0 = userVote.objects.filter(gameId = 1, day = 0)
    votes100 = userVote.objects.filter(gameId = 1, day = 100)
    votes101 = userVote.objects.filter(gameId = 1, day = 101)

    return render(request, "game.html", locals())


def post_game(request):
    if request.method == 'POST':
        # 传递所有游戏需要的post信息的接口
        gameId = 1
        response = request.META.get('HTTP_REFERER', '/')
        command = request.POST.get('action')
        if command == u'创建游戏':
            # 删除上一局的信息
            game_flag = True
            game = werewolf_game(str({}))
            userList = []
            tmp = Game2User.objects.filter(gameId = gameId)
            if tmp.count() < 12:
                game_flag = False
            i = 0
            for i in range(tmp.count()):
                if i < 12:
                    Game2User.objects.filter(gameId = gameId, user = tmp[i].user).update(seat = i)
                else:
                    Game2User.objects.filter(gameId = gameId, user = tmp[i].user).update(seat = -1)
                i = i + 1
            seatList = []
            for i in range(game.getNum()):
                seatList.append({})
            characters = game.characterList()
            for (seat, character) in characters:
                i = int(seat)
                seatList[i]['character'] = int(character)
                tmp = Game2User.objects.filter(gameId = gameId, seat = i)
                if len(tmp) == 1:
                    seatList[i]['user'] = Game2User.objects.filter(gameId = gameId, seat = i)[0].user
                else:
                    seatList[i]['user'] = request.user
                    game_flag = False

            # 新建一个游戏,并且保存到数据库中
            if game_flag:
                userVote.objects.filter(gameId = gameId).delete()
                Game2User.objects.filter(gameId = gameId).delete()
                for i in range(game.getNum()):
                    user = Game2User()
                    user.gameId = gameId
                    user.character = seatList[i]['character']
                    user.user = seatList[i]['user']
                    user.seat = i
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
        else:
            gameInfo = GameInfo.objects.filter(gameId = gameId)[0]
            game = werewolf_game(gameInfo.content)
            GameInfo.objects.filter(gameId = gameId).delete()
            if command == u'白天':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                game.GoThroughDay()

            if command == u'黑夜':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                game.GoThroughNight()

            if command == u'警左' or command == u'警右':
                SystemCommand.objects.filter(gameId = gameId).delete()
                list = game.getAliveList()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Speak'
                tmp['state'] = ''
                for i in range(game.getNum()):
                    if i in list:
                        tmp['state'] = tmp['state'] + '1'
                    else:
                        tmp['state'] = tmp['state'] + '0'
                if command == u'警左':
                    tmp['first'] = game.getPolice() - 1
                    if tmp['first'] < 0:
                        tmp['first'] = game.getNum() - 1
                else:
                    tmp['first'] = game.getPolice() + 1
                    if tmp['first'] >= game.getNum():
                        tmp['first'] = 0
                tmp['speaker'] = tmp['first']
                tmp['clockwise'] = randint(0, 1)
                syscommand.content = str(tmp)
                syscommand.save()

            if command == u'狼刀' or command == u'空刀':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                if command == u'狼刀':
                    tmp = request.POST.get('target')
                    if len(tmp) == 0:
                        target = -1
                    else:
                        target = int(tmp)
                    game.Wolf(target = target)
                else:
                    game.Wolf(target = -1)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Witch'
                syscommand.content = str(tmp)
                syscommand.save()
            if command == u'女巫救':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                game.witch(target = -1)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Seer'
                syscommand.content = str(tmp)
                syscommand.save()
            if command == u'女巫毒':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                target = int(request.POST.get('target'))
                game.witch(target = target)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Seer'
                syscommand.content = str(tmp)
                syscommand.save()
            if command == u'女巫过':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                game.witch(target = -2)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                tmp['command'] = 'Seer'
                syscommand.content = str(tmp)
                syscommand.save()
            if command == u'预言家':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                target = int(request.POST.get('target'))
                isWolf = game.seer(target = target)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand = SystemCommand()
                syscommand.gameId = gameId
                tmp = {}
                if game.getDay() == 1:
                    tmp['command'] = 'Police'
                    tmp['isWolf'] = isWolf
                else:
                    tmp['command'] = 'Day'
                    tmp['isWolf'] = isWolf
                syscommand.content = str(tmp)
                syscommand.save()

            if command == u'过':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                syscommand = SystemCommand.objects.filter(gameId = gameId)[0]
                SystemCommand.objects.filter(gameId = gameId).delete()
                tmp = eval(syscommand.content)
                s = tmp['state']
                tmp['state'] = ''
                if tmp['speaker'] > 0:
                    tmp['state'] = tmp['state'] + s[0 : tmp['speaker']]
                tmp['state'] = tmp['state'] + str(int(s[tmp['speaker']]) + 4)
                if tmp['speaker'] < game.getNum() - 1:
                    tmp['state'] = tmp['state'] + s[tmp['speaker'] + 1 : game.getNum()]
                if tmp['clockwise'] == 0:
                    tmp['speaker'] = tmp['speaker'] + 1
                    if tmp['speaker'] >= game.getNum():
                        tmp['speaker'] = 0
                else:
                    tmp['speaker'] = tmp['speaker'] - 1
                    if tmp['speaker'] < 0:
                        tmp['speaker'] = game.getNum() - 1
                syscommand.content = str(tmp)
                syscommand.save()

            if command == u'猎人开枪':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                target = int(request.POST.get('target'))
                game.hunter(target)
                syscommand = SystemCommand.objects.filter(gameId = gameId)[0]
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand.save()

            if command == u'狼人自爆':
                # 从数据库中拿出相应的游戏信息，处理后返回给数据库
                target = int(request.POST.get('target'))
                game.boom(target)
                syscommand = SystemCommand.objects.filter(gameId = gameId)[0]
                tmp = eval(syscommand.content)
                tmp['command'] = 'Werewolf'
                syscommand.content = str(tmp)
                SystemCommand.objects.filter(gameId = gameId).delete()
                syscommand.save()

            if command == u'上警' or command == u'不上警':
                vote = userVote()
                vote.seat = int(request.POST.get('voter'))
                if command == u'上警':
                    vote.vote = 1
                else:
                    vote.vote = 0
                vote.gameId = gameId
                vote.day = 100 # day == 100表示警上是否上警
                vote.save()
                votes = userVote.objects.filter(gameId = 1, day = 100)
                if len(votes) == game.getNum():
                    # 所有人都上警完毕
                    SystemCommand.objects.filter(gameId = gameId).delete()
                    syscommand = SystemCommand()
                    syscommand.gameId = gameId
                    tmp = {}
                    tmp['command'] = 'PoliceSpeak'
                    tmp['first'] = randint(0, game.getNum() - 1)
                    tmp['clockwise'] = randint(0, 1)
                    tmp['state'] = ''
                    w = []
                    for i in range(game.getNum()):
                        w.append('0')
                    for vote in votes:
                        w[vote.seat] = str(vote.vote)
                    for i in w:
                        tmp['state'] = tmp['state'] + i
                    tmp['speaker'] = tmp['first']
                    syscommand.content = str(tmp)
                    syscommand.save()

            if command == u'随机上警':
                userVote.objects.filter(gameId = 1, day = 100).delete()
                list = game.getAllList()
                for index in list:
                    vote = userVote()
                    vote.seat = index
                    vote.vote = randint(0, 1)
                    vote.gameId = gameId
                    vote.day = 100
                    vote.save()
                votes = userVote.objects.filter(gameId = 1, day = 100)
                if len(votes) == game.getNum():
                    # 所有人都上警完毕
                    SystemCommand.objects.filter(gameId = gameId).delete()
                    syscommand = SystemCommand()
                    syscommand.gameId = gameId
                    tmp = {}
                    tmp['command'] = 'PoliceSpeak'
                    tmp['first'] = randint(0, game.getNum() - 1)
                    tmp['speaker'] = tmp['first']
                    tmp['clockwise'] = randint(0, 1)
                    tmp['state'] = ''
                    w = []
                    for i in range(game.getNum()):
                        w.append('0')
                    for vote in votes:
                        w[vote.seat] = str(vote.vote)
                    for i in w:
                        tmp['state'] = tmp['state'] + i
                    syscommand.content = str(tmp)
                    syscommand.save()

            if command == u'投票' or command == u'警上投票':
                vote = userVote()
                vote.seat = int(request.POST.get('voter'))
                vote.vote = int(request.POST.get('target'))
                if vote.vote == None:
                    vote.vote = -1
                vote.gameId = gameId
                vote.day = game.getDay()
                if command == u'警上投票':
                    vote.day = 101
                vote.save()
                votes = userVote.objects.filter(gameId = gameId, day = vote.day)
                if len(votes) == game.getAliveNum():
                    # 所有人都投票完毕
                    exileP = -1
                    if command == u'警上投票':
                        tmp = []
                        for vote in votes:
                            tmp.append({'index': vote.seat, 'target' : vote.vote})
                        game.setPolice(tmp)
                    else:
                        tmp = []
                        for vote in votes:
                            tmp.append({'index': vote.seat, 'target' : vote.vote})
                        exileP = game.exile(tmp)
                    SystemCommand.objects.filter(gameId = gameId).delete()
                    syscommand = SystemCommand()
                    syscommand.gameId = gameId
                    tmp = {}
                    tmp['first'] = 0
                    tmp['speaker'] = 0
                    tmp['clockwise'] = 0
                    tmp['state'] = ''
                    deathList = game.getAllDeath()
                    if exileP != -1:
                        deathList.append(exileP)
                    for i in range(game.getNum()):
                        if i in deathList:
                            tmp['state'] = tmp['state'] + '1'
                        else:
                            tmp['state'] = tmp['state'] + '0'
                    if command == u'警上投票':
                        tmp['command'] = 'Last_words_Night'
                    else:
                        tmp['command'] = 'Last_words_Day'
                    syscommand.content = str(tmp)
                    syscommand.save()

            if command == u'随机投票' or command == u'随机警上投票':
                vote_day = game.getDay()
                if command == u'随机警上投票':
                    vote_day = 101
                userVote.objects.filter(gameId = gameId, day = vote_day).delete()
                list = game.getAliveList()
                for index in list:
                    vote = userVote()
                    vote.seat = index
                    vote.vote = game.randomAlive()
                    vote.gameId = gameId
                    vote.day = vote_day
                    vote.save()
                votes = userVote.objects.filter(gameId = gameId, day = vote_day)
                if len(votes) == game.getAliveNum():
                    # 所有人都投票完毕
                    exileP = -1
                    if command == u'随机警上投票':
                        tmp = []
                        for vote in votes:
                            tmp.append({'index': vote.seat, 'target' : vote.vote})
                        game.setPolice(tmp)
                    else:
                        tmp = []
                        for vote in votes:
                            tmp.append({'index': vote.seat, 'target' : vote.vote})
                        exileP = game.exile(tmp)
                    SystemCommand.objects.filter(gameId = gameId).delete()
                    syscommand = SystemCommand()
                    syscommand.gameId = gameId
                    tmp = {}
                    tmp['first'] = 0
                    tmp['speaker'] = 0
                    tmp['clockwise'] = 0
                    tmp['state'] = ''
                    deathList = game.getAllDeath()
                    if exileP != -1:
                        deathList.append(exileP)
                    for i in range(game.getNum()):
                        if i in deathList:
                            tmp['state'] = tmp['state'] + '1'
                        else:
                            tmp['state'] = tmp['state'] + '0'
                    if command == u'随机警上投票':
                        tmp['command'] = 'Last_words_Night'
                    else:
                        tmp['command'] = 'Last_words_Day'
                    syscommand.content = str(tmp)
                    syscommand.save()
            gameInfo.content = game.gameInfoEncode()
            gameInfo.save()
        return HttpResponseRedirect(response)
    else:
        raise Http404
