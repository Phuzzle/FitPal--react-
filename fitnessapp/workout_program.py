from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from fitnessapp.models import User, Exercise

class WorkoutProgram:
    def __init__(self, user_id, name, frequency, exercises):
        self.user_id = user_id
        self.name = name
        self.frequency = frequency
        self.exercises = exercises

    @staticmethod
    def create_program(user_id, name, frequency, exercises):
        # TODO: Implement program creation logic
        pass

    @staticmethod
    def get_program(program_id):
        # TODO: Implement program retrieval logic
        pass

    @staticmethod
    def update_program(program_id, updates):
        # TODO: Implement program update logic
        pass

    @staticmethod
    def delete_program(program_id):
        # TODO: Implement program deletion logic
        pass

def create_workout_program():
    @jwt_required()
    def wrapper():
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        required_fields = ['name', 'frequency', 'exercises']
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required data"}), 400

        name = data['name']
        frequency = data['frequency']
        exercises = data['exercises']

        # Validate frequency
        if frequency not in [3, 4, 5]:
            return jsonify({"message": "Invalid frequency. Choose 3, 4, or 5."}), 400

        # TODO: Validate exercises
        # TODO: Create the workout program
        # TODO: Save the workout program to the database

        return jsonify({"message": "Workout program created successfully"}), 201

    return wrapper

def get_available_exercises():
    @jwt_required()
    def wrapper():
        # TODO: Implement logic to get available exercises grouped by muscle group
        pass

    return wrapper
