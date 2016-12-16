from django.contrib import admin
from models import *

class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'nickname', 'age', 'gender', 'introduction', 'credit')

admin.site.register(Chat)
admin.site.register(GameInfo)
admin.site.register(Game2User)
admin.site.register(SystemCommand)
admin.site.register(room2Game)
admin.site.register(userVote, list_display = ('seat', 'day', 'vote'))
