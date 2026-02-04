from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to octofit_db'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Create Teams
        teams_data = [
            {
                "_id": "team_marvel",
                "name": "Team Marvel",
                "description": "Earth's Mightiest Heroes",
                "created_at": datetime.now(),
                "members": []
            },
            {
                "_id": "team_dc",
                "name": "Team DC",
                "description": "Justice League United",
                "created_at": datetime.now(),
                "members": []
            }
        ]
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams_data)} teams'))

        # Create Users (Superheroes)
        marvel_heroes = [
            {"name": "Tony Stark", "alias": "Iron Man", "email": "ironman@marvel.com", "team": "team_marvel"},
            {"name": "Steve Rogers", "alias": "Captain America", "email": "captainamerica@marvel.com", "team": "team_marvel"},
            {"name": "Natasha Romanoff", "alias": "Black Widow", "email": "blackwidow@marvel.com", "team": "team_marvel"},
            {"name": "Thor Odinson", "alias": "Thor", "email": "thor@marvel.com", "team": "team_marvel"},
            {"name": "Bruce Banner", "alias": "Hulk", "email": "hulk@marvel.com", "team": "team_marvel"},
            {"name": "Peter Parker", "alias": "Spider-Man", "email": "spiderman@marvel.com", "team": "team_marvel"},
        ]

        dc_heroes = [
            {"name": "Clark Kent", "alias": "Superman", "email": "superman@dc.com", "team": "team_dc"},
            {"name": "Bruce Wayne", "alias": "Batman", "email": "batman@dc.com", "team": "team_dc"},
            {"name": "Diana Prince", "alias": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "team_dc"},
            {"name": "Barry Allen", "alias": "The Flash", "email": "flash@dc.com", "team": "team_dc"},
            {"name": "Arthur Curry", "alias": "Aquaman", "email": "aquaman@dc.com", "team": "team_dc"},
            {"name": "Hal Jordan", "alias": "Green Lantern", "email": "greenlantern@dc.com", "team": "team_dc"},
        ]

        users_data = []
        for hero in marvel_heroes + dc_heroes:
            user = {
                "name": hero["name"],
                "alias": hero["alias"],
                "email": hero["email"],
                "team_id": hero["team"],
                "created_at": datetime.now() - timedelta(days=random.randint(30, 365)),
                "total_points": 0,
                "fitness_level": random.choice(["beginner", "intermediate", "advanced", "elite"])
            }
            users_data.append(user)

        db.users.insert_many(users_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users_data)} users'))

        # Update teams with member IDs
        marvel_user_ids = [user["email"] for user in users_data if user["team_id"] == "team_marvel"]
        dc_user_ids = [user["email"] for user in users_data if user["team_id"] == "team_dc"]

        db.teams.update_one({"_id": "team_marvel"}, {"$set": {"members": marvel_user_ids}})
        db.teams.update_one({"_id": "team_dc"}, {"$set": {"members": dc_user_ids}})

        # Create Workouts
        workouts_data = [
            {
                "name": "Super Soldier Strength Training",
                "description": "Captain America's legendary workout routine",
                "difficulty": "advanced",
                "duration_minutes": 60,
                "exercises": ["Push-ups", "Pull-ups", "Squats", "Burpees", "Planks"],
                "points": 100
            },
            {
                "name": "Stark Industries HIIT",
                "description": "High-intensity interval training designed by Tony Stark",
                "difficulty": "intermediate",
                "duration_minutes": 30,
                "exercises": ["Jumping Jacks", "Mountain Climbers", "High Knees", "Sprint Intervals"],
                "points": 75
            },
            {
                "name": "Asgardian Warrior Training",
                "description": "Thor's mighty hammer-wielding workout",
                "difficulty": "elite",
                "duration_minutes": 90,
                "exercises": ["Deadlifts", "Kettlebell Swings", "Battle Ropes", "Box Jumps"],
                "points": 150
            },
            {
                "name": "Speedster Cardio Blast",
                "description": "Flash's lightning-fast cardio routine",
                "difficulty": "intermediate",
                "duration_minutes": 45,
                "exercises": ["Sprint Intervals", "Jump Rope", "Cycling", "Stairs"],
                "points": 85
            },
            {
                "name": "Amazonian Combat Training",
                "description": "Wonder Woman's warrior workout",
                "difficulty": "advanced",
                "duration_minutes": 75,
                "exercises": ["Martial Arts", "Sword Training", "Shield Work", "Gymnastics"],
                "points": 120
            },
            {
                "name": "Web-Slinger Agility",
                "description": "Spider-Man's acrobatic training",
                "difficulty": "beginner",
                "duration_minutes": 30,
                "exercises": ["Stretching", "Balance Exercises", "Light Cardio", "Core Work"],
                "points": 50
            },
        ]

        db.workouts.insert_many(workouts_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_data)} workouts'))

        # Create Activities
        activities_data = []
        activity_types = ["run", "cycle", "swim", "strength", "yoga", "hike"]
        
        for user in users_data:
            # Create 5-10 activities per user
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                points = random.randint(10, 150)
                
                activity = {
                    "user_email": user["email"],
                    "user_alias": user["alias"],
                    "team_id": user["team_id"],
                    "activity_type": activity_type,
                    "duration_minutes": random.randint(15, 120),
                    "distance_km": round(random.uniform(1.0, 20.0), 2) if activity_type in ["run", "cycle", "swim", "hike"] else 0,
                    "calories_burned": random.randint(100, 800),
                    "points": points,
                    "date": datetime.now() - timedelta(days=random.randint(1, 30)),
                    "notes": f"{user['alias']} completed a {activity_type} session"
                }
                activities_data.append(activity)

        db.activities.insert_many(activities_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities_data)} activities'))

        # Update user total points based on activities
        for user in users_data:
            user_activities = [a for a in activities_data if a["user_email"] == user["email"]]
            total_points = sum(a["points"] for a in user_activities)
            db.users.update_one(
                {"email": user["email"]},
                {"$set": {"total_points": total_points}}
            )

        # Create Leaderboard entries
        leaderboard_data = []
        
        # Individual leaderboard
        sorted_users = sorted(users_data, key=lambda x: sum(a["points"] for a in activities_data if a["user_email"] == x["email"]), reverse=True)
        for rank, user in enumerate(sorted_users, 1):
            total_points = sum(a["points"] for a in activities_data if a["user_email"] == user["email"])
            leaderboard_data.append({
                "rank": rank,
                "type": "individual",
                "user_email": user["email"],
                "user_alias": user["alias"],
                "team_id": user["team_id"],
                "points": total_points,
                "updated_at": datetime.now()
            })

        # Team leaderboard
        marvel_points = sum(a["points"] for a in activities_data if a["team_id"] == "team_marvel")
        dc_points = sum(a["points"] for a in activities_data if a["team_id"] == "team_dc")

        team_rankings = [
            {"team_id": "team_marvel", "team_name": "Team Marvel", "points": marvel_points},
            {"team_id": "team_dc", "team_name": "Team DC", "points": dc_points}
        ]
        team_rankings.sort(key=lambda x: x["points"], reverse=True)

        for rank, team in enumerate(team_rankings, 1):
            leaderboard_data.append({
                "rank": rank,
                "type": "team",
                "team_id": team["team_id"],
                "team_name": team["team_name"],
                "points": team["points"],
                "updated_at": datetime.now()
            })

        db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_data)} leaderboard entries'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {db.users.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {db.teams.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {db.activities.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {db.workouts.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard: {db.leaderboard.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'\nTeam Marvel Points: {marvel_points}'))
        self.stdout.write(self.style.SUCCESS(f'Team DC Points: {dc_points}'))

        client.close()
