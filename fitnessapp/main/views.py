from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from fitnessapp.models import User, Exercise
from fitnessapp.workout_program import create_workout_program, get_available_exercises
from . import main

@main.route('/')
def index():
    return "Welcome to the Fitness App!"

@main.route('/add_workout', methods=['POST'])
@jwt_required()
def add_workout():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    workout_data = request.get_json()
    if not workout_data:
        return jsonify({"message": "No workout data provided"}), 400

    required_fields = ['type', 'duration', 'intensity']
    if not all(field in workout_data for field in required_fields):
        return jsonify({"message": "Missing required workout data"}), 400

    user.add_workout(workout_data)
    return jsonify({"message": "Workout added successfully"}), 201

@main.route('/get_workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    limit = request.args.get('limit', default=10, type=int)
    workouts = user.get_workouts(limit)
    return jsonify({"workouts": workouts}), 200

@main.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    recent_workouts = user.get_workouts(limit=5)
    workout_stats = user.get_workout_stats()
    
    return jsonify({
        "user_email": user.email,
        "recent_workouts": recent_workouts,
        "workout_stats": workout_stats
    }), 200

@main.route('/workout_stats', methods=['GET'])
@jwt_required()
def workout_stats():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    stats = user.get_workout_stats()
    if not stats:
        return jsonify({"message": "No workout data available"}), 404

    return jsonify(stats), 200

@main.route('/exercises', methods=['POST'])
@jwt_required()
def create_exercise():
    exercise_data = request.get_json()
    if not exercise_data:
        return jsonify({"message": "No exercise data provided"}), 400

    required_fields = ['name', 'type', 'muscle_group', 'description', 'instructions']
    if not all(field in exercise_data for field in required_fields):
        return jsonify({"message": "Missing required exercise data"}), 400

    new_exercise = Exercise.create_exercise(**exercise_data)
    exercise_dict = new_exercise.to_dict()
    return jsonify({"message": "Exercise created successfully", "exercise": exercise_dict}), 201

@main.route('/exercises/<exercise_id>', methods=['GET'])
@jwt_required()
def get_exercise(exercise_id):
    exercise = Exercise.get_exercise_by_id(exercise_id)
    if not exercise:
        return jsonify({"message": "Exercise not found"}), 404
    return jsonify(exercise.to_dict()), 200

@main.route('/exercises/muscle_group/<muscle_group>', methods=['GET'])
@jwt_required()
def get_exercises_by_muscle_group(muscle_group):
    exercises = Exercise.get_exercises_by_muscle_group(muscle_group)
    return jsonify([exercise.to_dict() for exercise in exercises]), 200

@main.route('/exercises/<exercise_id>', methods=['PUT'])
@jwt_required()
def update_exercise(exercise_id):
    exercise = Exercise.get_exercise_by_id(exercise_id)
    if not exercise:
        return jsonify({"message": "Exercise not found"}), 404

    update_data = request.get_json()
    if not update_data:
        return jsonify({"message": "No update data provided"}), 400

    # Validate the update data
    allowed_fields = ['name', 'type', 'muscle_group', 'description', 'instructions', 'default_weight', 'default_sets', 'default_reps']
    for key in update_data.keys():
        if key not in allowed_fields:
            return jsonify({"message": f"Invalid field: {key}"}), 400

    exercise.update(**update_data)
    return jsonify({"message": "Exercise updated successfully", "exercise": exercise.to_dict()}), 200

@main.route('/exercises', methods=['GET'])
@jwt_required()
def list_exercises():
    exercises = Exercise.get_all_exercises()
    return jsonify([exercise.to_dict() for exercise in exercises]), 200

@main.route('/record_exercise', methods=['POST'])
@jwt_required()
def record_exercise():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ['exercise_id', 'weight', 'sets', 'reps']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required data"}), 400

    exercise_id = data['exercise_id']
    weight = data['weight']
    sets = data['sets']
    reps = data['reps']

    user.record_exercise_completion(exercise_id, weight, sets, reps)
    return jsonify({"message": "Exercise recorded successfully"}), 201

@main.route('/exercise_history/<exercise_id>', methods=['GET'])
@jwt_required()
def get_exercise_history(exercise_id):
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    history = user.get_exercise_history(exercise_id)
    if history:
        return jsonify(history), 200
    else:
        return jsonify({"message": "No history found for this exercise"}), 404

@main.route('/create_workout_program', methods=['POST'])
@jwt_required()
def create_program():
    return create_workout_program()

@main.route('/available_exercises', methods=['GET'])
@jwt_required()
def available_exercises():
    return get_available_exercises()
