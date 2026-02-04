# OctoFit Tracker API Documentation

## Base URL
`http://localhost:8000`

## API Endpoints

### Root
- **GET** `/` - API Root information with available endpoints

### Users
- **GET** `/api/users/` - List all users
- **POST** `/api/users/` - Create a new user
- **GET** `/api/users/{id}/` - Get user details
- **PUT** `/api/users/{id}/` - Update user
- **PATCH** `/api/users/{id}/` - Partial update user
- **DELETE** `/api/users/{id}/` - Delete user
- **GET** `/api/users/top_performers/` - Get top 10 users by points

**Filters:** `team_id`, `fitness_level`  
**Search:** `name`, `alias`, `email`  
**Ordering:** `total_points`, `created_at`, `name`

### Teams
- **GET** `/api/teams/` - List all teams
- **POST** `/api/teams/` - Create a new team
- **GET** `/api/teams/{id}/` - Get team details
- **PUT** `/api/teams/{id}/` - Update team
- **PATCH** `/api/teams/{id}/` - Partial update team
- **DELETE** `/api/teams/{id}/` - Delete team
- **GET** `/api/teams/{id}/members/` - Get all team members
- **GET** `/api/teams/{id}/activities/` - Get all team activities

**Search:** `name`, `description`  
**Ordering:** `name`, `created_at`

### Activities
- **GET** `/api/activities/` - List all activities
- **POST** `/api/activities/` - Create a new activity
- **GET** `/api/activities/{id}/` - Get activity details
- **PUT** `/api/activities/{id}/` - Update activity
- **PATCH** `/api/activities/{id}/` - Partial update activity
- **DELETE** `/api/activities/{id}/` - Delete activity
- **GET** `/api/activities/recent/` - Get 20 most recent activities
- **GET** `/api/activities/by_user/?email={email}` - Get activities by user email

**Filters:** `user_email`, `team_id`, `activity_type`  
**Search:** `user_alias`, `notes`  
**Ordering:** `date`, `points`, `duration_minutes`, `distance_km`

### Workouts
- **GET** `/api/workouts/` - List all workouts
- **POST** `/api/workouts/` - Create a new workout
- **GET** `/api/workouts/{id}/` - Get workout details
- **PUT** `/api/workouts/{id}/` - Update workout
- **PATCH** `/api/workouts/{id}/` - Partial update workout
- **DELETE** `/api/workouts/{id}/` - Delete workout
- **GET** `/api/workouts/by_difficulty/?difficulty={level}` - Get workouts by difficulty

**Filters:** `difficulty`  
**Search:** `name`, `description`  
**Ordering:** `points`, `duration_minutes`, `name`

### Leaderboard
- **GET** `/api/leaderboard/` - List all leaderboard entries
- **GET** `/api/leaderboard/{id}/` - Get leaderboard entry details
- **GET** `/api/leaderboard/individual/` - Get individual rankings
- **GET** `/api/leaderboard/team/` - Get team rankings
- **GET** `/api/leaderboard/top_ten/` - Get top 10 individual rankings

**Filters:** `type`, `team_id`  
**Ordering:** `rank`, `points`

### Admin
- **GET** `/admin/` - Django admin interface

## Data Models

### User
```json
{
  "_id": "ObjectId",
  "name": "string",
  "alias": "string",
  "email": "string (unique)",
  "team_id": "string",
  "created_at": "datetime",
  "total_points": "integer",
  "fitness_level": "beginner|intermediate|advanced|elite"
}
```

### Team
```json
{
  "_id": "string",
  "name": "string",
  "description": "string",
  "created_at": "datetime",
  "members": ["email1", "email2"]
}
```

### Activity
```json
{
  "_id": "ObjectId",
  "user_email": "string",
  "user_alias": "string",
  "team_id": "string",
  "activity_type": "run|cycle|swim|strength|yoga|hike",
  "duration_minutes": "integer",
  "distance_km": "float",
  "calories_burned": "integer",
  "points": "integer",
  "date": "datetime",
  "notes": "string"
}
```

### Workout
```json
{
  "_id": "ObjectId",
  "name": "string",
  "description": "string",
  "difficulty": "beginner|intermediate|advanced|elite",
  "duration_minutes": "integer",
  "exercises": ["exercise1", "exercise2"],
  "points": "integer"
}
```

### Leaderboard
```json
{
  "_id": "ObjectId",
  "rank": "integer",
  "type": "individual|team",
  "user_email": "string (optional)",
  "user_alias": "string (optional)",
  "team_id": "string (optional)",
  "team_name": "string (optional)",
  "points": "integer",
  "updated_at": "datetime"
}
```

## Running the Server

1. Activate virtual environment:
   ```bash
   source octofit-tracker/backend/venv/bin/activate
   ```

2. Run the development server:
   ```bash
   cd octofit-tracker/backend
   python manage.py runserver 0.0.0.0:8000
   ```

   Or use the VS Code debugger: "Launch Django Backend"

3. Access the API:
   - API Root: http://localhost:8000/
   - Admin Interface: http://localhost:8000/admin/
   - Users: http://localhost:8000/api/users/
   - Teams: http://localhost:8000/api/teams/
   - Activities: http://localhost:8000/api/activities/
   - Workouts: http://localhost:8000/api/workouts/
   - Leaderboard: http://localhost:8000/api/leaderboard/

## Testing

Run tests:
```bash
python manage.py test octofit_tracker
```

## Database Management

Populate database with sample data:
```bash
python manage.py populate_db
```
