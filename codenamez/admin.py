from django.contrib import admin

from codenamez.models import UserData, Game

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', 'avatar', 'game', 'options')

class GameAdmin(admin.ModelAdmin):
    list_display = ('game', 'name', 'created', 'started', 'ended', 'cancelled')

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Game, GameAdmin)
