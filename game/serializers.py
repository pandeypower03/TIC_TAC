from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Move, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class MoveSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)

    class Meta:
        model = Move
        fields = ('id', 'game', 'player', 'position_x', 'position_y', 'created_at')
        read_only_fields = ('game', 'player')

class GameSerializer(serializers.ModelSerializer):
    player1 = UserSerializer(read_only=True)
    player2 = UserSerializer(read_only=True)
    current_turn = UserSerializer(read_only=True)
    winner = UserSerializer(read_only=True)
    moves = MoveSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'player1', 'player2', 'current_turn', 'board', 'status', 'winner', 'created_at', 'updated_at', 'moves')
        read_only_fields = ('board', 'status', 'winner')

class GameHistorySerializer(serializers.ModelSerializer):
    opponent = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    player1_name = serializers.CharField(source='player1.username')
    player2_name = serializers.CharField(source='player2.username')
    winner_name = serializers.CharField(source='winner.username', allow_null=True)

    class Meta:
        model = Game
        fields = ('id', 'player1_name', 'player2_name', 'winner_name', 'opponent', 'result', 'created_at')

    def get_opponent(self, obj):
        request = self.context.get('request')
        if request.user == obj.player1:
            return UserSerializer(obj.player2).data
        return UserSerializer(obj.player1).data

    def get_result(self, obj):
        request = self.context.get('request')
        if obj.status != 'completed':
            return 'ongoing'
        if obj.winner is None:
            return 'draw'
        return 'won' if obj.winner == request.user else 'lost'

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    win_rate = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('username', 'bio', 'games_played', 'games_won', 'games_lost', 
                 'games_drawn', 'win_rate', 'created_at', 'updated_at')
        read_only_fields = ('games_played', 'games_won', 'games_lost', 
                          'games_drawn', 'created_at', 'updated_at')

    def get_win_rate(self, obj):
        if obj.games_played == 0:
            return 0
        return round((obj.games_won / obj.games_played) * 100, 2)

class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = ('username', 'bio')
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        if profile_data:
            profile = instance.profile
            profile.bio = profile_data.get('bio', profile.bio)
            profile.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
