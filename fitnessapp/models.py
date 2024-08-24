from config import db
from firebase_admin import firestore
import datetime

class User:
    def __init__(self, user_id, email, password_hash):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.account_created = firestore.SERVER_TIMESTAMP
        self.last_login = firestore.SERVER_TIMESTAMP

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
