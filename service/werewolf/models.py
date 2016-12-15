from django.db import models
from django.contrib.auth.models import User

class Game2User(models.Model):
    gameId = models.IntegerField(default=0)
    seat = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='sitting')
    character = models.IntegerField(default=0)
    def __unicode__(self):
        return u'%s' % self.id

class GameInfo(models.Model):
    gameId = models.IntegerField(default=0)
    content = models.TextField(default = '{}')
    def __unicode__(self):
        return u'%s' % self.id

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats')
    gameId = models.IntegerField(default=0)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.content

class SystemCommand(models.Model):
    gameId = models.IntegerField(default=0)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.content

class room2Game(models.Model):
    roomnum = models.IntegerField(default=0)
    gameId = models.IntegerField(default=0)
    def __unicode__(self):
        return u'(%d, %d)' % (self.roomnum, self.gameId)