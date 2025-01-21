from django.contrib import admin
from .models import Game, Move, UserProfile

# Register your models here.

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'winner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('player1__username', 'player2__username')
    date_hierarchy = 'created_at'

@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'player', 'position_x', 'position_y', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('game__id', 'player__username')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'games_played', 'games_won', 'games_lost', 'games_drawn')
    search_fields = ('user__username',)
