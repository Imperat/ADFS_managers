from django.contrib import admin

from teamlogic import models


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    date_hierarchy = 'birth'
    list_display = ('__str__', 'vk_link', 'birth')
    list_editable = ('vk_link',)
    list_filter = ('history', 'basePosition')
    search_fields = ['lastName']


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'foundation', 'vk_link', 'captain', 'home')
    list_editable = ('vk_link', 'captain', 'home')


@admin.register(models.TeamInLeague)
class TeamInLeagueAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'goal_s', 'goal_p', 'match_v',
                    'match_n', 'match_p', 'penalty', 'get_points')
    list_editable = ('penalty',)
    list_filter = ('league',)


@admin.register(models.MatchInLeague)
class MatchInLeagueAdmin(admin.ModelAdmin):
    list_display = ('home', 'away', 'home_goal', 'away_goal',
                    'home_goal_first', 'away_goal_first',
                    'league', 'tour', 'hasResult', 'register')

    list_editable = ('hasResult', 'tour')
    list_filter = ('league', 'tour')


@admin.register(models.Tournament)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'begin_date', 'end_date')
    fields = ('name', 'begin_date', 'end_date', 'image', 'members2')


admin.site.register(models.RecOfTeam)
admin.site.register(models.Stadium)
admin.site.register(models.Match)
admin.site.register(models.Goal)
admin.site.register(models.TimeBoard)

admin.sites.AdminSite.index_template = 'admin/index.html'
