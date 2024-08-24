from config import db
from firebase_admin import firestore
import datetime
from statistics import mean

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
            return User(user_data['user_id'], user_data['email'], user_data['password_hash'])
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
            return User(user_data['user_id'], user_data['email'], user_data['password_hash'])
        return None
