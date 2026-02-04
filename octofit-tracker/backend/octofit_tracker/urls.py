"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import UserViewSet, TeamViewSet, ActivityViewSet, WorkoutViewSet, LeaderboardViewSet
import os

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'workouts', WorkoutViewSet, basename='workout')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')


@api_view(['GET'])
def api_root(request):
    """
    OctoFit Tracker API Root
    
    Available endpoints:
    - /api/users/ - User management
    - /api/teams/ - Team management
    - /api/activities/ - Activity tracking
    - /api/workouts/ - Workout library
    - /api/leaderboard/ - Competition rankings
    """
    # Get CODESPACE_NAME environment variable
    codespace_name = os.environ.get('CODESPACE_NAME')
    
    # Build base URL based on environment
    if codespace_name:
        base_url = f'https://{codespace_name}-8000.app.github.dev'
    else:
        base_url = request.build_absolute_uri('/').rstrip('/')
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0',
        'endpoints': {
            'users': f'{base_url}/api/users/',
            'teams': f'{base_url}/api/teams/',
            'activities': f'{base_url}/api/activities/',
            'workouts': f'{base_url}/api/workouts/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'admin': f'{base_url}/admin/',
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
