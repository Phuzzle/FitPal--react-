from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from fitnessapp.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User.create_user(email, hashed_password)

    return jsonify({"message": "User registered successfully", "user_id": new_user.user_id}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.get_user_by_email(email)
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    user.update_last_login()
    access_token = create_access_token(identity=user.user_id)
    return jsonify({"access_token": access_token}), 200

@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "account_created": user.account_created.isoformat() if user.account_created else None,
        "last_login": user.last_login.isoformat() if user.last_login else None
    }), 200
