from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard


class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'alias', 'email', 'team_id', 'team_name', 'created_at', 'total_points', 'fitness_level']
        read_only_fields = ['_id', 'created_at']
    
    def get_team_name(self, obj):
        """Get the team name for this user"""
        if obj.team_id:
            try:
                team = Team.objects.get(_id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return None


class TeamSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'members', 'member_count']
        read_only_fields = ['created_at']
    
    def get_member_count(self, obj):
        """Get actual count of users in this team"""
        return User.objects.filter(team_id=obj._id).count()


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_email', 'user_alias', 'team_id', 'activity_type', 
                  'duration_minutes', 'distance_km', 'calories_burned', 'points', 
                  'date', 'notes']
        read_only_fields = ['_id']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'difficulty', 'duration_minutes', 
                  'exercises', 'points']
        read_only_fields = ['_id']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['_id', 'rank', 'type', 'user_email', 'user_alias', 'team_id', 
                  'team_name', 'points', 'updated_at']
        read_only_fields = ['_id', 'updated_at']
