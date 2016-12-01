from django.contrib import admin
from models import Chat

class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'nickname', 'age', 'gender', 'introduction', 'credit')

admin.site.register(Chat)
