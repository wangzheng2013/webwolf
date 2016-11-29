# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.core.context_processors import csrf
from django import forms

class userInfoForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput())

def test(request):
    return render(request, 'account/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return HttpResponseRedirect('/signup/', username)
    if request.method == 'GET':
        username = request.GET.get('username')
        return render(request, 'account/signup.html', locals())
    return render(request, 'account/signup.html', locals())