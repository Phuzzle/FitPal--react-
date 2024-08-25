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
        exercise_counts = {
            "Compound, pec-dominant": 2,
            "Compound, shoulder-dominant": 2,
            "Compound, upper back horizontal": 2,
            "Compound, upper back vertical": 2,
            "Compound, hip-dominant": 1,
            "Compound, knee-dominant": 1,
            "Calves": 2,
            "Hip-dominant accessory": 1,
            "Quad-dominant accessory": 1
        }

        selected_exercises = {}
        for exercise in exercises:
            for category, exercise_list in EXERCISE_CATEGORIES.items():
                if exercise in exercise_list:
                    if category not in selected_exercises:
                        selected_exercises[category] = []
                    selected_exercises[category].append(exercise)
                    break

        # Check if the correct number of exercises are selected for each category
        for category, count in exercise_counts.items():
            if category not in selected_exercises or len(selected_exercises[category]) != count:
                return jsonify({"message": f"Invalid exercise selection. Please select {count} exercise(s) from {category}"}), 400

        # Flatten the selected exercises list
        final_exercises = [exercise for sublist in selected_exercises.values() for exercise in sublist]

        # Create the workout program
        program = WorkoutProgram.create_program(current_user_id, name, frequency, final_exercises)

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
