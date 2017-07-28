#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.db import models

from utils.helpers import NULLABLE

class ADFSUser(User):
    avatar = models.ImageField(upload_to="media",
                               default="./404/profile.jpg", **NULLABLE)

    objects = UserManager()

class Attention(models.Model):

    name = models.CharField(
        max_length=40, verbose_name='Имя и Фамилия:', null=True)

    vkLink = models.CharField(
        max_length=40, verbose_name='Ссылка на ваш профиль в вк:', null=True)

    phone = models.CharField(
        max_length=12, verbose_name='Контактный телефон для связи:', null=True)

    # Information about team
    avatar = models.ImageField(verbose_name='Эмблема команды:', null=True)
    team = models.CharField(
        verbose_name='Название команды:', max_length=10, null=True)

    grundung = models.DateField(
        verbose_name='Год основания команды:',
        null=True,
        help_text='Если ваша команда была основана ранее, укажите год')

    sostav = models.FileField(
        verbose_name='Напишите список игроков. Одна строчка - один игрок.'
                     'Соблюдайте формат заявок - обработка автоматическая.',
        help_text="3 Лионель Аршавин 11.04.1993")

    regl = models.BooleanField(default=True)
    first_league = models.BooleanField(
        verbose_name='Первая лига АДФС 2016', default=True)

    pokal = models.BooleanField(
        verbose_name='Кубок АДФС 2016', default=True)

    winter_pokal = models.BooleanField(
        verbose_name='Зимний кубок АДФС 2015/16', default=True)

    def get_absolute_url(self):
        return reverse('attention', args=(self.id,))

    def __unicode__(self):
        return u"Заявка: %s %s" % (self.name, self.team)
