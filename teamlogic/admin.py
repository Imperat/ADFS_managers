from django.contrib import admin

from teamlogic import models

from easy_select2 import select2_modelform

@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Player, attrs={'width': '250px'})
    date_hierarchy = 'birth'
    list_display = ('__str__', 'vk_link', 'birth')
    list_editable = ('vk_link',)
    list_filter = ('history', 'basePosition')
    search_fields = ['lastName']


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Team, attrs={'width': '250px'})
    list_display = ('name', 'foundation', 'vk_link', 'captain', 'home')
    list_editable = ('vk_link', 'captain', 'home')


@admin.register(models.TeamInLeague)
class TeamInLeagueAdmin(admin.ModelAdmin):
    form = select2_modelform(models.TeamInLeague, attrs={'width': '250px'})
    list_display = ('team', 'league', 'goal_s', 'goal_p', 'match_v',
                    'match_n', 'match_p', 'penalty', 'get_points')
    list_editable = ('penalty',)
    list_filter = ('league',)


@admin.register(models.MatchInLeague)
class MatchInLeagueAdmin(admin.ModelAdmin):
    form = select2_modelform(models.MatchInLeague, attrs={'width': '250px'})
    list_display = ('home', 'away', 'home_goal', 'away_goal',
                    'home_goal_first', 'away_goal_first',
                    'league', 'tour', 'hasResult', 'register')

    list_editable = ('hasResult', 'tour')
    list_filter = ('league', 'tour')


@admin.register(models.Tournament)
class LeagueAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Tournament, attrs={'width': '250px'})
    list_display = ('name', 'begin_date', 'end_date', '__str__',
                    'get_season')
    fields = ('name', 'begin_date', 'end_date', 'image', 'members2')

@admin.register(models.Cup)
class CupAdmin(admin.ModelAdmin):
    form = select2_modelform(models.Cup, attrs={'width': '250px'})

@admin.register(models.MatchPair)
class MatchPair(admin.ModelAdmin):
    form = select2_modelform(models.MatchPair, attrs={'width': '250px'})


@admin.register(models.RecOfTeam)
class RecOfTeamAdmin(admin.ModelAdmin):
    form = select2_modelform(models.RecOfTeam, attrs={'width': '250px'})
    fields=('beginDate', 'endDate', 'team', 'player', 'number', 'isActive')
    list_filter = ('team',)


admin.site.register(models.Stadium)
admin.site.register(models.Match)
admin.site.register(models.Goal)
admin.site.register(models.TimeBoard)

admin.sites.AdminSite.index_template = 'admin/index.html'
