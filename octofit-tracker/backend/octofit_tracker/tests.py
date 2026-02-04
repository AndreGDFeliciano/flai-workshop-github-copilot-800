from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Workout, Leaderboard
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name="Peter Parker",
            alias="Spider-Man",
            email="spiderman@marvel.com",
            team_id="team_marvel",
            total_points=100,
            fitness_level="intermediate"
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.name, "Peter Parker")
        self.assertEqual(self.user.alias, "Spider-Man")
        self.assertEqual(str(self.user), "Spider-Man (spiderman@marvel.com)")
    
    def test_user_email_unique(self):
        """Test email uniqueness constraint"""
        with self.assertRaises(Exception):
            User.objects.create(
                name="Miles Morales",
                alias="Spider-Man",
                email="spiderman@marvel.com",  # Duplicate email
                team_id="team_marvel",
                fitness_level="beginner"
            )


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            _id="team_marvel",
            name="Team Marvel",
            description="Earth's Mightiest Heroes",
            members=["ironman@marvel.com", "captainamerica@marvel.com"]
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, "Team Marvel")
        self.assertEqual(len(self.team.members), 2)
        self.assertEqual(str(self.team), "Team Marvel")


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_email': 'thor@marvel.com',
            'user_alias': 'Thor',
            'team_id': 'team_marvel',
            'activity_type': 'strength',
            'duration_minutes': 60,
            'distance_km': 0,
            'calories_burned': 500,
            'points': 100,
            'date': datetime.now().isoformat(),
            'notes': 'Asgardian strength training'
        }
    
    def test_create_activity(self):
        """Test creating a new activity via API"""
        url = reverse('activity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().user_alias, 'Thor')
    
    def test_list_activities(self):
        """Test listing all activities"""
        Activity.objects.create(**self.activity_data)
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name="Super Soldier Training",
            description="Captain America's workout",
            difficulty="advanced",
            duration_minutes=60,
            exercises=["Push-ups", "Pull-ups", "Squats"],
            points=100
        )
    
    def test_list_workouts(self):
        """Test listing all workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_difficulty(self):
        """Test filtering workouts by difficulty"""
        url = reverse('workout-by-difficulty')
        response = self.client.get(url, {'difficulty': 'advanced'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.individual_entry = Leaderboard.objects.create(
            rank=1,
            type='individual',
            user_email='superman@dc.com',
            user_alias='Superman',
            team_id='team_dc',
            points=1000
        )
        self.team_entry = Leaderboard.objects.create(
            rank=1,
            type='team',
            team_id='team_dc',
            team_name='Team DC',
            points=5000
        )
    
    def test_list_leaderboard(self):
        """Test listing all leaderboard entries"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_individual_leaderboard(self):
        """Test getting individual leaderboard only"""
        url = reverse('leaderboard-individual')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'individual')
    
    def test_team_leaderboard(self):
        """Test getting team leaderboard only"""
        url = reverse('leaderboard-team')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type'], 'team')


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_api_root(self):
        """Test API root endpoint returns correct information"""
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
        self.assertEqual(response.data['message'], 'Welcome to OctoFit Tracker API')
