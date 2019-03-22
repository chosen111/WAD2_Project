from django.contrib import admin

from codenamez.models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', 'avatar', 'options', 'games_won', 'games_lost', 'games_played', 'ranking')

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created', 'visible', 'deleted')

class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'message', 'created', 'visible', 'deleted')

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'max_players', 'created', 'started', 'ended', 'cancelled')

class GamePlayerAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'points', 'team', 'joined', 'is_admin', 'is_spymaster')

class WordListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(PrivateMessage, PrivateMessageAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GamePlayer, GamePlayerAdmin)
admin.site.register(WordList, WordListAdmin)
