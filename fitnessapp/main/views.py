from . import main

@main.route('/')
def index():
    return "Hello, World!"

# Add more route handlers here
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from fitnessapp.models import User

main = Blueprint('main', __name__)

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
    # You can add more dashboard data here, such as workout statistics, goals, etc.
    
    return jsonify({
        "user_email": user.email,
        "recent_workouts": recent_workouts,
        # Add more dashboard data here
    }), 200
