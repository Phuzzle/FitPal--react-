from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from fitnessapp.models import User, Exercise
from config import db

EXERCISE_CATEGORIES = {
    "Compound, pec-dominant": [
        "Barbell Bench Press",
        "Dumbbell Bench Press",
        "Incline Dumbbell Press",
        "Push-ups"
    ],
    "Compound, shoulder-dominant": [
        "Overhead Press (Barbell)",
        "Seated Dumbbell Press",
        "Push Press",
        "Arnold Press"
    ],
    "Compound, upper back horizontal": [
        "Barbell Row",
        "Pendlay Row",
        "Chest-Supported Row (Dumbbell)",
        "Bent-Over Row (Dumbbell)"
    ],
    "Compound, upper back vertical": [
        "Pull-Ups",
        "Lat Pulldowns",
        "Close-Grip Lat Pulldown"
    ],
    "Compound, hip-dominant": [
        "Deadlifts",
        "Romanian Deadlifts (RDLs)",
        "Barbell Hip Thrust",
        "Good Mornings"
    ],
    "Compound, knee-dominant": [
        "Barbell Back Squat",
        "Front Squat",
        "Bulgarian Split Squat",
        "Walking Lunges"
    ],
    "Hip-dominant accessory": [
        "Glute Bridges",
        "Single-Leg RDLs",
        "Barbell Hip Thrust",
        "Glute Ham Raises"
    ],
    "Quad-dominant accessory": [
        "Goblet Squats",
        "Step-Ups",
        "Bulgarian Split Squats",
        "Wall Sit"
    ],
    "Calves": [
        "Standing Calf Raises (Barbell)",
        "Seated Calf Raises (Dumbbell)",
        "Single-Leg Calf Raises"
    ],
    "Vanity lifts": [
        "Dumbbell Flyes",
        "Barbell Curls",
        "Skullcrushers",
        "Crunches",
        "Shrugs",
        "Lateral Raise (Dumbbell)"
    ]
}

class WorkoutProgram:
    def __init__(self, user_id, name, frequency, exercises):
        self.user_id = user_id
        self.name = name
        self.frequency = frequency
        self.exercises = exercises

    @staticmethod
    def create_program(user_id, name, frequency, exercises):
        program_ref = db.collection('workout_programs').document()
        program_id = program_ref.id
        program_data = {
            'user_id': user_id,
            'name': name,
            'frequency': frequency,
            'exercises': exercises
        }
        program_ref.set(program_data)
        return WorkoutProgram(user_id, name, frequency, exercises)

    @staticmethod
    def get_program(program_id):
        program_ref = db.collection('workout_programs').document(program_id)
        program_doc = program_ref.get()
        if program_doc.exists:
            program_data = program_doc.to_dict()
            return WorkoutProgram(
                program_data['user_id'],
                program_data['name'],
                program_data['frequency'],
                program_data['exercises']
            )
        return None

    @staticmethod
    def update_program(program_id, updates):
        program_ref = db.collection('workout_programs').document(program_id)
        program_ref.update(updates)

    @staticmethod
    def delete_program(program_id):
        program_ref = db.collection('workout_programs').document(program_id)
        program_ref.delete()

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

        # Validate exercises
        valid_exercises = [exercise for category in EXERCISE_CATEGORIES.values() for exercise in category]
        if not all(exercise in valid_exercises for exercise in exercises):
            return jsonify({"message": "Invalid exercise selection"}), 400

        # Create the workout program
        program = WorkoutProgram.create_program(current_user_id, name, frequency, exercises)

        return jsonify({
            "message": "Workout program created successfully",
            "program": {
                "name": program.name,
                "frequency": program.frequency,
                "exercises": program.exercises
            }
        }), 201

    return wrapper

def get_available_exercises():
    @jwt_required()
    def wrapper():
        return jsonify(EXERCISE_CATEGORIES), 200

    return wrapper
