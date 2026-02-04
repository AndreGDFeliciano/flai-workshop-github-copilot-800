from djongo import models


class User(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    total_points = models.IntegerField(default=0)
    fitness_level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('elite', 'Elite'),
    ])

    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return f"{self.alias} ({self.email})"


class Team(models.Model):
    _id = models.CharField(max_length=100, primary_key=True, db_column='_id')
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.JSONField(default=list)

    class Meta:
        db_table = 'teams'
        
    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    user_email = models.EmailField()
    user_alias = models.CharField(max_length=200)
    team_id = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=50, choices=[
        ('run', 'Run'),
        ('cycle', 'Cycle'),
        ('swim', 'Swim'),
        ('strength', 'Strength'),
        ('yoga', 'Yoga'),
        ('hike', 'Hike'),
    ])
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(default=0)
    calories_burned = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.user_alias} - {self.activity_type} - {self.date}"


class Workout(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('elite', 'Elite'),
    ])
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)
    points = models.IntegerField()

    class Meta:
        db_table = 'workouts'
        
    def __str__(self):
        return f"{self.name} ({self.difficulty})"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    rank = models.IntegerField()
    type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('team', 'Team'),
    ])
    user_email = models.EmailField(blank=True, null=True)
    user_alias = models.CharField(max_length=200, blank=True, null=True)
    team_id = models.CharField(max_length=100, blank=True, null=True)
    team_name = models.CharField(max_length=200, blank=True, null=True)
    points = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        
    def __str__(self):
        if self.type == 'individual':
            return f"#{self.rank} - {self.user_alias} ({self.points} pts)"
        else:
            return f"#{self.rank} - {self.team_name} ({self.points} pts)"
