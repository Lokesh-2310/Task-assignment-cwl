from flask import Blueprint, request, jsonify
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from jwtutils import create_jwt, decode_jwt
from mongodb_creation import get_user_collection 

auth_bp = Blueprint("auth", __name__)


# ===================== TOKEN REQUIRED DECORATOR =====================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwt_token")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        user_data = decode_jwt(token)
        if not user_data:
            return jsonify({"error": "Token invalid or expired"}), 401

        return f(user_data, *args, **kwargs)

    return decorated


# ===================== SIGNUP ROUTE =====================
@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    
    users_col = get_user_collection()

    # Check if user exists in MongoDB
    existing_user = users_col.find_one({"email": email})

    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = generate_password_hash(password)

    user_doc = {
        "name": name,
        "email": email,
        "password": hashed_pw
    }

    users_col.insert_one(user_doc)

    return jsonify({"message": "Signup successful. You can now login."}), 201


# ===================== LOGIN ROUTE =====================
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")
    
    users_col = get_user_collection()

    user = users_col.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token
    token = create_jwt(str(user["_id"]), user["email"])

    return jsonify({"message": "Login success", "token": token}), 200

