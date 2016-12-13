# -*- coding: utf-8 -*-
# 狼人游戏逻辑模块

from aenum import Enum
from random import randint

class gameLog():
    log = []
    def addLog(self, str):
        self.log.append(str)
    def show(self):
        for message in self.log:
            print(message)

class werewolf_character():

    class CHARACTER(Enum):
        NULL = 0, 'NULL'
        WEREWOLF = 1, 'WEREWOLF'
        VILLEGER = 2, 'VILLEGER'
        SEER = 3, 'SEER'
        WITCH = 4, 'WITCH'
        HUNTER = 5, 'HUNTER'
        IDIOT = 6, 'IDIOT'
        def __new__(cls, value, name):
            member = object.__new__(cls)
            member._value_ = value
            member.fullname = name
            return member

        def __int__(self):
            return self.value

        def __str__(self):
            return self.name

    class DEATH(Enum):
        NULL = 0
        METHERED_BY_WOLVES = 1
        EXILE = 2
        POISONED_BY_WITCH = 3
        SHOOTED_BY_HUNTER = 4

    character = CHARACTER.NULL
    alive = True
    death_noticed = True
    def __init__(self, character):
        self.alive = True
        self.character = character

    def __str__(self):
        return "character : %d" % self.character

    def isWolf(self):
        return self.character == self.CHARACTER.WEREWOLF
    def isGold(self):
        return (self.character == self.CHARACTER.HUNTER) or (self.character == self.CHARACTER.SEER) or (self.character == self.CHARACTER.WITCH) or (self.character == self.CHARACTER.IDIOT)
    def isVilleger(self):
        return self.character == self.CHARACTER.VILLEGER
    def isHunter(self):
        return self.character == self.CHARACTER.HUNTER
    def isSeer(self):
        return self.character == self.CHARACTER.SEER
    def isWitch(self):
        return self.character == self.CHARACTER.WITCH
    def isIdiot(self):
        return self.character == self.CHARACTER.IDIOT

class werewolf_game():
    """ 狼人游戏 对象 """
    __day = 0
    __num = 12
    __WitchAntidote = True
    __WitchPoison = True
    __HunterGun = True
    __IdiotFaceUp = False
    __victim = 0
    __Police = -1
    gameId = 0 # 游戏id对应储存在数据库的游戏列表ID
    log = gameLog()
    character = []
    def __init__(self):
        """无先决条件，新建一个GAME"""
        self.gameId = 1
        self.__day = 0
        self.__num = 12
        self.__WitchAntidote = True
        self.__WitchPoison = True
        self.__HunterGun = True

        # 初始化所有角色
        for i in range(4):
            self.character.append(werewolf_character(werewolf_character.CHARACTER.VILLEGER))
            self.character.append(werewolf_character(werewolf_character.CHARACTER.WEREWOLF))
        self.character.append(werewolf_character(werewolf_character.CHARACTER.WITCH))
        self.character.append(werewolf_character(werewolf_character.CHARACTER.HUNTER))
        self.character.append(werewolf_character(werewolf_character.CHARACTER.SEER))
        self.character.append(werewolf_character(werewolf_character.CHARACTER.IDIOT))
        for i in range(12):
            j = randint(0, i)
            tmp = self.character[i]
            self.character[i] = self.character[j]
            self.character[j] = tmp
        # 保存角色
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #

    def kill(self, index, flag):
        """角色死亡，触发死亡技能等"""
        # FLAG 参数为 死亡状态 参照 werewolf_character.DEATH
        self.character[index].alive = False
        self.character[index].death_noticed = False
        if (self.character[index].isHunter()):
            # 猎人死亡
            if flag != werewolf_character.DEATH.POISONED_BY_WITCH:
                # 可以开枪
                self.hunter()
            else:
                # 不可开枪
                self.character[index].alive = False

        if (self.character[index].isIdiot() and flag == werewolf_character.DEATH.EXILE):
            self.character[index].alive = True
            self.__IdiotFaceUp = True
            self.log.addLog(u"God : %d号玩家为白痴神身份，免于放逐并变为灵魂状态"%index)

    def canVote(self, index):
        # 判定一个人是否有放逐投票的资格
        if self.character[index].isIdiot():
            return not self.__IdiotFaceUp
        else:
            return self.character[index].alive

    def isFinished(self):
        """ 判定游戏是否结束 """
        countW = 0
        countV = 0
        countG = 0
        for i in range(self.__num):
            if (not self.character[i].alive):
                continue
            if (self.character[i].isWolf()):
                countW = countW + 1
            if (self.character[i].isGold()):
                countG = countG + 1
            if (self.character[i].isVilleger()):
                countV = countV + 1
        if (countV == 0 or countG == 0):
            return 1 # 屠边结束， 狼人获胜
        if (countW == 0):
            return 2 # 游戏结束， 好人获胜
        return 0

    def show(self):
        """ 展示游戏状态 """
        for i in range(self.__num):
            print(i, self.character[i].alive, self.character[i].character)
        print("WitchAntidote : ", self.__WitchAntidote)
        print("WitchPoison : ", self.__WitchPoison)
        print("HunterGun : ", self.__HunterGun)
        print("IdiotFaceUp : ", self.__IdiotFaceUp)

    def Wolf(self):
        """ 狼人执行技能 """
        # 是否存在狼人,存在则询问狼是否杀人
        tmp = 0
        for i in range(self.__num):
            if (self.character[i].isWolf()) and (self.character[i].alive):
                tmp = tmp + 1
        if (tmp == 0):
            return
        killPlayer = randint(0, 11)
        while (not self.character[killPlayer].alive):
            killPlayer = randint(0, 11)
        self.log.addLog('wolves decided to kill %dth player' % killPlayer)
        self.__victim = killPlayer

    def seer(self):
        """ 预言家执行技能 """
        # 是否存在预言家,存在则询问
        tmp = 0
        for i in range(self.__num):
            if (self.character[i].isSeer()) and (self.character[i].alive):
                tmp = tmp + 1
        if (tmp == 0):
            return
        seePlayer = randint(0, 11)
        self.log.addLog('seer decided to predict %dth player' % seePlayer)

    def witch(self):
        """ 女巫执行技能 """
        # 是否存在女巫,存在则询问
        victim = self.__victim
        tmp = 0
        for i in range(self.__num):
            if (self.character[i].isWitch()) and (self.character[i].alive):
                tmp = tmp + 1
        if (tmp == 0):
            self.kill(victim, werewolf_character.DEATH.METHERED_BY_WOLVES)
            return
        flag = True
        if (self.__WitchAntidote):
            # 女巫可以使用解药
            if randint(0, 1) == 0:
                # 使用解药
                self.log.addLog('witch decided to help %dth player' % victim)
                self.__WitchAntidote = False
                flag = False
        if (flag):
            # 女巫没有不救或者没药
            self.kill(victim, werewolf_character.DEATH.METHERED_BY_WOLVES)

        if (flag and self.__WitchPoison):
            if randint(0, 1) == 0:
                # 使用毒药
                self.__WitchPoison = False
                killPlayer = randint(0, 11)
                while (not self.character[killPlayer].alive):
                    killPlayer = randint(0, 11)
                self.log.addLog('witch decided to poison %dth player' % killPlayer)
                self.kill(killPlayer, werewolf_character.DEATH.POISONED_BY_WITCH)

    def hunter(self):
        """ 猎人执行技能 ： 执行条件满足后才会进入，不需判定执行前置条件 """
        if (self.__HunterGun):
            killPlayer = randint(0, 11)
            while (not self.character[killPlayer].alive):
                killPlayer = randint(0, 11)
            self.log.addLog('hunter decided to shoot %dth player' % killPlayer)
            self.kill(killPlayer, werewolf_character.DEATH.SHOOTED_BY_HUNTER)
            self.__HunterGun = False

    def GoThroughNight(self):
        """ 晚上各角色执行技能 """
        if (self.isFinished()):
            return
        self.__day = self.__day + 1
        self.log.addLog('night %d' % self.__day)
        # 狼人杀人
        self.Wolf()
        # 预言家验人
        self.seer()
        # 女巫救人和毒人
        self.witch()

    def GoThroughDay(self):
        if (self.isFinished() != 0):
            return
        """ 白天轮转 """
        if (self.__day == 1):
            # 警上竞选
            join_in = [] # 0 警下 1 警上 2 退水
            self.log.addLog("joining in : ")
            for i in range(self.__num):
                join_in.append(randint(0, 1))
                if join_in[-1] == 1:
                    self.log.addLog("%dth player joining in"% i)
            first = randint(0, self.__num - 1)
            if (randint(0, 1) == 0):
                # 顺时针发言
                self.log.addLog("God : %dth player started to make a speech(clockwise)" % first)
                for i in range(self.__num):
                    index = (i + first) % self.__num
                    if join_in[index] == 1:
                        # 上警了
                        self.log.addLog("%dth player made a speech" % index)

            else:
                # 逆时针发言
                self.log.addLog("God : %dth player started to make a speech(anticlockwise)" % first)
                for i in range(self.__num):
                    index = (self.__num + first - i) % self.__num
                    if join_in[index] == 1:
                        # 上警了
                        self.log.addLog("%dth player made a speech" % index)

            count = 0
            for i in range(self.__num):
                count = count + join_in[i]
            tmp = [] # 得票数量
            for i in range(self.__num):
                tmp.append(0)
            if (count > 0) and (count < self.__num):
                # 竞选， 警徽
                maxn = 0
                for i in range(self.__num):
                    # 投票
                    if join_in[i] != 0:
                        continue
                    w = randint(0, self.__num - 1)
                    while (join_in[w] != 1):
                        w = randint(0, self.__num - 1)
                    self.log.addLog("%dth player choose %dth player"%(i, w))
                    tmp[w] = tmp[w] + 1
                    if tmp[w] > maxn:
                        maxn = tmp[w]

                # 对最大票数的人数进行统计
                wnum = 0
                for j in range(self.__num):
                    if tmp[j] == maxn:
                        wnum = wnum + 1
                        self.__Police = j
                self.log.addLog(u"最大票数共%d人"% wnum)
                if wnum == 1:
                    # 只有一个警长，顺利竞选完毕
                    self.log.addLog(u"God : %d号玩家当选警长"%self.__Police)

                if wnum > 1:
                    # 平票
                    self.log.addLog("God : REJUDGE")
                    for j in range(self.__num):
                        if (tmp[j] != maxn) and (join_in[j] == 1):
                            join_in[j] = 2
                        tmp[j] = 0
                    maxn = 0
                    for j in range(self.__num):
                        if join_in[j] == 0:
                            w = randint(0, self.__num - 1)
                            while (join_in[w] != 1):
                                w = randint(0, self.__num - 1)
                            tmp[w] = tmp[w] + 1
                            if tmp[w] > maxn:
                                maxn = tmp[w]
                            self.log.addLog("%dth player choose %dth player"%(j, w))
                    wnum = 0
                    for j in range(self.__num):
                        if tmp[j] == maxn:
                            wnum = wnum + 1
                            self.__Police = j
                    if wnum == 1:
                        # 只有一个警长，顺利竞选完毕
                        self.log.addLog(u"God : %d号玩家当选警长"%self.__Police)
                    else:
                        # 警徽流失
                        self.log.addLog(u"God : 没有警徽")
                        self.__Police = -1
            else:
                self.log.addLog(u"God : 没有警徽")
        # 宣布昨夜情况
        self.log.addLog('day %d' % self.__day)
        minn_death = -1
        for i in range(self.__num):
            if (not self.character[i].death_noticed) and (not self.character[i].alive):
                self.log.addLog(u'God : 昨夜%d号玩家死亡' % i)
                if self.__day == 1:
                    self.log.addLog("%dth player made a speech" % i)
                self.character[i].death_noticed = True
                if (minn_death == -1):
                    minn_death = i
        if minn_death == -1:
            self.log.addLog(u'God : 昨夜平安夜')
        if self.isFinished() == 1:
            self.log.addLog(u'God : 游戏结束， 狼人获胜')
        if self.isFinished() == 2:
            self.log.addLog(u'God : 游戏结束， 好人获胜')
        if (self.isFinished() != 0):
            return
        first = 0
        if self.__Police != -1:
            first = (self.__Police + 1) % self.__num
        else:
            first = (minn_death + 1) % self.__num
        for i in range(self.__num):
            index = (first + i) % self.__num
            if self.character[index].alive:
                self.log.addLog("%dth player made a speech" % index)

        killPlayer = randint(0, 11)
        while (not self.character[killPlayer].alive):
            killPlayer = randint(0, 11)
        self.log.addLog('%dth player exile' % killPlayer)
        self.kill(killPlayer, werewolf_character.DEATH.EXILE)

    # 导出信息
    def characterList(self):
        list = []
        for i in range(self.__num):
            list.append((i, self.character[i].character))
        return list