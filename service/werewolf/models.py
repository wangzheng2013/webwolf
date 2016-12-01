from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    def __unicode__(self):
        return u'%s' % self.id

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='has_chats')
    gameId = models.IntegerField(default=0)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self):
        return u'%s' % self.content

