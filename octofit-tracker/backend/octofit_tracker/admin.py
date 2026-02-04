from django.contrib import admin
from .models import User, Team, Activity, Workout, Leaderboard


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('alias', 'name', 'email', 'team_id', 'total_points', 'fitness_level', 'created_at')
    list_filter = ('team_id', 'fitness_level', 'created_at')
    search_fields = ('name', 'alias', 'email')
    ordering = ('-total_points',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'alias', 'email')
        }),
        ('Team & Performance', {
            'fields': ('team_id', 'total_points', 'fitness_level')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)
    
    def member_count(self, obj):
        return len(obj.members) if obj.members else 0
    member_count.short_description = 'Members'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_alias', 'activity_type', 'duration_minutes', 'distance_km', 
                    'calories_burned', 'points', 'date', 'team_id')
    list_filter = ('activity_type', 'team_id', 'date')
    search_fields = ('user_alias', 'user_email', 'notes')
    ordering = ('-date',)
    date_hierarchy = 'date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_email', 'user_alias', 'team_id')
        }),
        ('Activity Details', {
            'fields': ('activity_type', 'duration_minutes', 'distance_km', 'calories_burned', 'points')
        }),
        ('Additional Information', {
            'fields': ('date', 'notes')
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration_minutes', 'points', 'exercise_count')
    list_filter = ('difficulty',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    def exercise_count(self, obj):
        return len(obj.exercises) if obj.exercises else 0
    exercise_count.short_description = 'Exercises'
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('name', 'description', 'difficulty')
        }),
        ('Workout Details', {
            'fields': ('duration_minutes', 'exercises', 'points')
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'type', 'get_name', 'points', 'updated_at')
    list_filter = ('type', 'team_id')
    search_fields = ('user_alias', 'team_name', 'user_email')
    ordering = ('rank',)
    readonly_fields = ('updated_at',)
    
    def get_name(self, obj):
        if obj.type == 'individual':
            return obj.user_alias
        else:
            return obj.team_name
    get_name.short_description = 'Name'
    
    fieldsets = (
        ('Ranking', {
            'fields': ('rank', 'type', 'points')
        }),
        ('Individual Details', {
            'fields': ('user_email', 'user_alias'),
            'classes': ('collapse',),
        }),
        ('Team Details', {
            'fields': ('team_id', 'team_name'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )


# Customize admin site header and title
admin.site.site_header = "OctoFit Tracker Administration"
admin.site.site_title = "OctoFit Admin Portal"
admin.site.index_title = "Welcome to OctoFit Tracker Admin"
