from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player2')
    current_turn = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_current_turn')
    board = models.JSONField(default=list)  # Stores the 3x3 board as a list of lists
    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ], default='ongoing')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='games_won')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id}: {self.player1.username} vs {self.player2.username}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.board:  # Only initialize board if it's a new game
            self.board = [[None, None, None] for _ in range(3)]
        super().save(*args, **kwargs)

class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Move by {self.player.username} at ({self.position_x}, {self.position_y})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    games_drawn = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def update_game_stats(self, result):
        self.games_played += 1
        if result == 'won':
            self.games_won += 1
        elif result == 'lost':
            self.games_lost += 1
        elif result == 'draw':
            self.games_drawn += 1
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
