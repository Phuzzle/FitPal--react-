from config import db
from firebase_admin import firestore
import datetime
from statistics import mean

from uuid import uuid4

class Exercise:
    def __init__(self, name, type, muscle_group, description, instructions, 
                 default_weight=None, default_sets=3, default_reps=10, exercise_id=None):
        self.exercise_id = exercise_id
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
        exercise_ref = db.collection('exercises').document()
        exercise_id = exercise_ref.id
        exercise = Exercise(name, type, muscle_group, description, instructions, 
                            default_weight, default_sets, default_reps, exercise_id)
        exercise_ref.set(exercise.to_dict())
        return exercise

    @staticmethod
    def get_exercise_by_id(exercise_id):
        exercise_ref = db.collection('exercises').document(exercise_id)
        exercise_doc = exercise_ref.get()
        if exercise_doc.exists:
            exercise_data = exercise_doc.to_dict()
            exercise = Exercise(
                name=exercise_data['name'],
                type=exercise_data['type'],
                muscle_group=exercise_data['muscle_group'],
                description=exercise_data['description'],
                instructions=exercise_data['instructions'],
                default_weight=exercise_data.get('default_weight'),
                default_sets=exercise_data.get('default_sets', 3),
                default_reps=exercise_data.get('default_reps', 10)
            )
            exercise.exercise_id = exercise_id
            return exercise
        return None

    @staticmethod
    def get_exercises_by_muscle_group(muscle_group):
        exercises_ref = db.collection('exercises').where('muscle_group', '==', muscle_group)
        exercises = []
        for doc in exercises_ref.stream():
            exercise_data = doc.to_dict()
            exercise = Exercise(
                name=exercise_data['name'],
                type=exercise_data['type'],
                muscle_group=exercise_data['muscle_group'],
                description=exercise_data['description'],
                instructions=exercise_data['instructions'],
                default_weight=exercise_data.get('default_weight'),
                default_sets=exercise_data.get('default_sets', 3),
                default_reps=exercise_data.get('default_reps', 8)
            )
            exercise.exercise_id = doc.id
            exercises.append(exercise)
        return exercises

    @staticmethod
    def get_all_exercises():
        exercises_ref = db.collection('exercises')
        exercises = []
        for doc in exercises_ref.stream():
            exercise_data = doc.to_dict()
            exercise = Exercise(
                name=exercise_data['name'],
                type=exercise_data['type'],
                muscle_group=exercise_data['muscle_group'],
                description=exercise_data['description'],
                instructions=exercise_data['instructions'],
                default_weight=exercise_data.get('default_weight'),
                default_sets=exercise_data.get('default_sets', 3),
                default_reps=exercise_data.get('default_reps', 8)
            )
            exercise.exercise_id = doc.id
            exercises.append(exercise)
        return exercises

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if self.exercise_id:
            exercise_ref = db.collection('exercises').document(self.exercise_id)
            exercise_ref.update(self.to_dict())

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

    def add_workout(self, workout_data):
        workouts_ref = db.collection('users').document(self.user_id).collection('workouts').document()
        workouts_ref.set(workout_data)

    def get_workouts(self, limit=10):
        workouts_ref = db.collection('users').document(self.user_id).collection('workouts')
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

    def record_exercise_completion(self, exercise_id, weight, sets, reps):
        exercise_completion = {
            'exercise_id': exercise_id,
            'weight': weight,
            'sets': sets,
            'reps': reps,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        db.collection('users').document(self.user_id).collection('exercise_completions').add(exercise_completion)

    def get_exercise_history(self, exercise_id):
        completions_ref = db.collection('users').document(self.user_id).collection('exercise_completions')
        query = completions_ref.where('exercise_id', '==', exercise_id).order_by('timestamp', direction=firestore.Query.DESCENDING)
        return [doc.to_dict() for doc in query.stream()]

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
            )
        return None
