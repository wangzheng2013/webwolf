"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from werewolf.views import *
from werewolf.views_SignIO import *
from werewolf.view_room import *
from werewolf.view_game import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', Home),
    # room
    url(r'^room/$', room),
    url(r'^chat/$', chat),
    url(r'^get_chat/$', get_chat),
    url(r'^post_chat/$', post_chat),
    # game
    url(r'^game_api/$', game_api),
    url(r'^post_game/$', post_game),
    # userBase
    url(r'^userbase/$', userbase),
    # sign/log IO
    url(r'^test/$', test),
    url(r'^logout/$', logout),
    url(r'^login/$', login),
    url(r'^signup/$', signup)
]
