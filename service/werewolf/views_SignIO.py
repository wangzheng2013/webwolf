# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.core.context_processors import csrf
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth


class userInfoForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput())

def test(request):
    return render(request, 'account/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        states = 'success'
        if password != password2:
            states = 'difference'
        if len(User.objects.filter(username=username)) > 0:
            states = 'exist'
        if states == 'success':
            user= User()
            user.username = username
            user.set_password(password)
            user.email = ''
            user.save()
        return HttpResponseRedirect('/signup/?states='+states+'&username=' + username)
    if request.method == 'GET':
        states = request.GET.get('states')
        message = r'欢迎注册'.decode('utf-8')
        if states != None:
            username = request.GET.get('username')
            if states == 'success':
                message = username + r'注册成功'.decode('utf-8')
            if states == 'difference':
                message = username + r'注册失败，密码两次输入的密码不相同'.decode('utf-8')
            if states == 'exist':
                message = username + r'注册失败，用户名已存在'.decode('utf-8')
        return render(request, 'account/signup.html', locals())
    return render(request, 'account/signup.html', locals())

def userbase(request):
    #username = request.get('username')
    username = request.user.username
    return render(request, "userbase.html", locals())

def logout(request):
    response = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return HttpResponseRedirect(response)

def login(request):
    response = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
    return HttpResponseRedirect(response)
