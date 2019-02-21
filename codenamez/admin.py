from django.contrib import admin

from codenamez.models import UserProfile, Chat, PrivateMessage, Game, GameList

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', 'avatar', 'options')

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created', 'visible', 'deleted')

class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'message', 'created', 'visible', 'deleted')

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'max_players', 'created', 'started', 'ended', 'cancelled')

class GameListAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'points', 'team', 'joined')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(PrivateMessage, PrivateMessageAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameList, GameListAdmin)
