from django.contrib import admin

from codenamez.models import UserProfile, Game, GameList

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', 'avatar', 'options')

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'started', 'ended', 'cancelled')

class GameListAdmin(admin.ModelAdmin):
    list_display = ('game', 'user')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameList, GameListAdmin)
