from config import db
from firebase_admin import firestore
import datetime
from statistics import mean

from uuid import uuid4

class Exercise:
    def __init__(self, name, type, muscle_group, description, instructions, 
                 default_weight=None, default_sets=3, default_reps=10):
        self.exercise_id = str(uuid4())
        self.name = name
        self.type = type
        self.muscle_group = muscle_group
        self.description = description
        self.instructions = instructions
        self.default_weight = default_weight
        self.default_sets = default_sets
        self.default_reps = default_reps

    @staticmethod
    def create_exercise(name, type, muscle_group, description, instructions, 
                        default_weight=None, default_sets=3, default_reps=10):
        # This method would interact with the database to create a new exercise
        exercise = Exercise(name, type, muscle_group, description, instructions, 
                            default_weight, default_sets, default_reps)
        # Here you would save the exercise to the database
        return exercise

    @staticmethod
    def get_exercise_by_id(exercise_id):
        # This method would retrieve an exercise from the database by its ID
        # For now, we'll return None to indicate it's not implemented
        return None

    @staticmethod
    def get_exercises_by_muscle_group(muscle_group):
        # This method would retrieve all exercises for a specific muscle group
        # For now, we'll return an empty list to indicate it's not implemented
        return []

    def update(self, **kwargs):
        # This method would update the exercise's attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # Here you would save the updated exercise to the database

    def to_dict(self):
        return {
            'exercise_id': self.exercise_id,
            'name': self.name,
            'type': self.type,
            'muscle_group': self.muscle_group,
            'description': self.description,
            'instructions': self.instructions,
            'default_weight': self.default_weight,
            'default_sets': self.default_sets,
            'default_reps': self.default_reps
        }

class User:
    def __init__(self, user_id, email, password_hash, account_created=None, last_login=None):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.account_created = account_created
        self.last_login = last_login

    @staticmethod
    def create_user(email, password_hash):
        user_ref = db.collection('users').document()
        user_data = {
            'user_id': user_ref.id,
            'email': email,
            'password_hash': password_hash,
            'account_created': firestore.SERVER_TIMESTAMP,
            'last_login': firestore.SERVER_TIMESTAMP
        }
        user_ref.set(user_data)
        return User(user_ref.id, email, password_hash)

    @staticmethod
    def get_user_by_email(email):
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1)
        results = query.get()
        for doc in results:
            user_data = doc.to_dict()
            return User(
                user_data['user_id'],
                user_data['email'],
                user_data['password_hash'],
                user_data.get('account_created'),
                user_data.get('last_login')
            )
        return None

    def update_last_login(self):
        user_ref = db.collection('users').document(self.user_id)
        user_ref.update({'last_login': firestore.SERVER_TIMESTAMP})

    def add_workout(self, workout_data):
        workouts_ref = db.collection('users').document(self.user_id).collection('workouts').document()
        workout_data['timestamp'] = firestore.SERVER_TIMESTAMP
        workouts_ref.set(workout_data)

    def get_workouts(self, limit=10):
        workouts_ref = db.collection('users').document(self.user_id).collection('workouts')
        query = workouts_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        return [doc.to_dict() for doc in query.get()]

    def get_workout_stats(self):
        workouts = self.get_workouts(limit=100)  # Get the last 100 workouts for stats
        if not workouts:
            return None

        total_duration = sum(workout.get('duration', 0) for workout in workouts)
        avg_duration = total_duration / len(workouts)

        workout_types = {}
        for workout in workouts:
            workout_type = workout.get('type', 'Unknown')
            workout_types[workout_type] = workout_types.get(workout_type, 0) + 1

        most_common_type = max(workout_types, key=workout_types.get)

        return {
            'total_workouts': len(workouts),
            'avg_duration': avg_duration,
            'most_common_type': most_common_type,
            'type_distribution': workout_types
        }

    @staticmethod
    def get_user_by_id(user_id):
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(
                user_data['user_id'],
                user_data['email'],
                user_data['password_hash'],
                user_data.get('account_created'),
                user_data.get('last_login')
            )
        return None
