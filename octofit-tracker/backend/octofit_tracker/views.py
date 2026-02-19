from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Workout, Leaderboard
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer, 
    WorkoutSerializer, LeaderboardSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    Supports list, create, retrieve, update, and delete operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team_id', 'fitness_level']
    search_fields = ['name', 'alias', 'email']
    ordering_fields = ['total_points', 'created_at', 'name']
    ordering = ['-total_points']

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 10 users by total points"""
        top_users = User.objects.all().order_by('-total_points')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

# potato potato
class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing teams.
    Supports list, create, retrieve, update, and delete operations.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team_id=team._id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific team"""
        team = self.get_object()
        activities = Activity.objects.filter(team_id=team._id)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing activities.
    Supports list, create, retrieve, update, and delete operations.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'team_id', 'activity_type']
    search_fields = ['user_alias', 'notes']
    ordering_fields = ['date', 'points', 'duration_minutes', 'distance_km']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get most recent 20 activities"""
        recent_activities = Activity.objects.all().order_by('-date')[:20]
        serializer = self.get_serializer(recent_activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user by email"""
        email = request.query_params.get('email', None)
        if email:
            activities = Activity.objects.filter(user_email=email).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter required'}, status=400)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing workouts.
    Supports list, create, retrieve, update, and delete operations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['points', 'duration_minutes', 'name']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Difficulty parameter required'}, status=400)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing leaderboard.
    Supports list and retrieve operations primarily.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'team_id']
    ordering_fields = ['rank', 'points']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def individual(self, request):
        """Get individual leaderboard rankings"""
        individual_rankings = Leaderboard.objects.filter(type='individual').order_by('rank')
        serializer = self.get_serializer(individual_rankings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def team(self, request):
        """Get team leaderboard rankings"""
        team_rankings = Leaderboard.objects.filter(type='team').order_by('rank')
        serializer = self.get_serializer(team_rankings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_ten(self, request):
        """Get top 10 individual rankings"""
        top_ten = Leaderboard.objects.filter(type='individual').order_by('rank')[:10]
        serializer = self.get_serializer(top_ten, many=True)
        return Response(serializer.data)
