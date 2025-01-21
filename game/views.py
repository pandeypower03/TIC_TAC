from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Game, Move, UserProfile
from .serializers import (
    GameSerializer, UserSerializer, GameHistorySerializer,
    UserProfileSerializer, UserRegistrationSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Exclude the current user from the list
        return User.objects.exclude(id=self.request.user.id)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        serializer = UserRegistrationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserProfileSerializer(request.user.profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsGameParticipant()]
        return [IsAuthenticated()]

    def create(self, request):
        player2_id = request.data.get('player2_id')
        if not player2_id:
            return Response(
                {'error': 'player2_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        player2 = get_object_or_404(User, id=player2_id)
        if player2 == request.user:
            return Response(
                {'error': 'Cannot play against yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        game = Game.objects.create(
            player1=request.user,
            player2=player2,
            current_turn=request.user,
            board=[[None, None, None] for _ in range(3)]
        )

        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def make_move(self, request, pk=None):
        game = self.get_object()
        if game.status != 'ongoing':
            return Response({'error': 'Game is already finished'}, status=status.HTTP_400_BAD_REQUEST)

        if game.current_turn != request.user:
            return Response({'error': 'Not your turn'}, status=status.HTTP_400_BAD_REQUEST)

        x = request.data.get('position_x')
        y = request.data.get('position_y')

        if not (0 <= x < 3 and 0 <= y < 3):
            return Response({'error': 'Invalid position'}, status=status.HTTP_400_BAD_REQUEST)

        if game.board[x][y] is not None:
            return Response({'error': 'Position already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Make the move
        symbol = 'X' if request.user == game.player1 else 'O'
        game.board[x][y] = symbol
        
        # Record the move
        Move.objects.create(game=game, player=request.user, position_x=x, position_y=y)

        # Check for winner
        def check_winner():
            # Check rows
            for i in range(3):
                if game.board[i][0] == game.board[i][1] == game.board[i][2] and game.board[i][0] is not None:
                    return True
            # Check columns
            for i in range(3):
                if game.board[0][i] == game.board[1][i] == game.board[2][i] and game.board[0][i] is not None:
                    return True
            # Check diagonals
            if game.board[0][0] == game.board[1][1] == game.board[2][2] and game.board[0][0] is not None:
                return True
            if game.board[0][2] == game.board[1][1] == game.board[2][0] and game.board[0][2] is not None:
                return True
            return False

        def is_board_full():
            return all(cell is not None for row in game.board for cell in row)

        if check_winner():
            game.status = 'completed'
            game.winner = request.user
            # Update player profiles
            request.user.profile.update_game_stats('won')
            other_player = game.player2 if request.user == game.player1 else game.player1
            other_player.profile.update_game_stats('lost')
        elif is_board_full():
            game.status = 'completed'
            # Update player profiles for draw
            if game.status == 'completed' and not game.winner:
                game.player1.profile.update_game_stats('draw')
                game.player2.profile.update_game_stats('draw')
        else:
            game.current_turn = game.player2 if request.user == game.player1 else game.player1

        game.save()
        return Response(GameSerializer(game).data)

    @action(detail=False, methods=['get'])
    def my_games(self, request):
        """
        Get the user's game history with detailed information about:
        - Opponent details
        - Game result (win/loss/draw)
        - Timeline of moves made during the match
        """
        games = Game.objects.filter(Q(player1=request.user) | Q(player2=request.user))
        serializer = GameHistorySerializer(games, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        if game.status != 'ongoing':
            return Response(
                {'error': 'Cannot update completed games'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        game = serializer.instance
        if game.status == 'completed':
            # Update player profiles when game is completed
            winner = game.winner
            if winner:
                winner.profile.update_game_stats('won')
                loser = game.player1 if winner == game.player2 else game.player2
                loser.profile.update_game_stats('lost')
            else:
                game.player1.profile.update_game_stats('draw')
                game.player2.profile.update_game_stats('draw')
        serializer.save()

class MatchHistoryView(generics.ListAPIView):
    serializer_class = GameHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Game.objects.filter(
            Q(player1=self.request.user) | Q(player2=self.request.user)
        ).order_by('-created_at')
