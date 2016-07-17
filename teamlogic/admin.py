from django.contrib import admin
from models import *
# Register your models here.


class PlayerAdmin(admin.ModelAdmin):
    date_hierarchy = 'birth'
    list_display = ('__unicode__', 'vk_link', 'birth')
    list_editable = ('vk_link',)
    list_filter = ('history', 'basePosition')
    search_fields = ['lastName']


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'foundation', 'vk_link', 'captain', 'home')
    list_editable = ('vk_link', 'captain', 'home')


class TeamInLeagueAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'goal_s', 'goal_p', 'match_v',
                    'match_n', 'match_p', 'penalty', 'get_points')
    list_editable = ('penalty',)
    list_filter = ('league',)


class MatchInLeagueAdmin(admin.ModelAdmin):
    list_display = ('home', 'away', 'home_goal', 'away_goal', 'home_goal_first',
                    'away_goal_first', 'league', 'tour', 'hasResult', 'register')
    list_editable = ('hasResult',)
    list_filter = ('league', 'tour')


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'begin_date', 'end_date')
    fields = ('name', 'begin_date', 'end_date', 'image')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(RecOfTeam)
admin.site.register(Stadium)
admin.site.register(Match)
admin.site.register(Goal)

admin.site.register(Tournament, LeagueAdmin)
admin.site.register(TeamInLeague, TeamInLeagueAdmin)
admin.site.register(MatchInLeague, MatchInLeagueAdmin)

admin.sites.AdminSite.index_template = 'admin/index.html'
