from django.contrib import admin

# Register your models here.

from werewolf.models import *


class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'nickname', 'age', 'gender', 'introduction', 'credit')

admin.site.register(User, userAdmin)
admin.site.register(Contact)
