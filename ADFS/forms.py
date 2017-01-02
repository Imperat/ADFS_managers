#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    vkLink = forms.CharField(label='Профиль в вк', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=10)
    team = forms.CharField(label='Название команды', max_length=32)
    first_league = forms.BooleanField(required=False)
    pokal = forms.BooleanField(required=False)
    winter_pokal = forms.BooleanField(required=False)
