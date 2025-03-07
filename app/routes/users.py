from flask import Blueprint, jsonify, request
from app.database import get_connection
from app.queries import CREATE_USERS_TABLE, INSERT_USER_RETURN_ID

users_bp = Blueprint('users', __name__)

@users_bp.route("/api/user", methods=["POST"])
def create_user():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            try:
                cursor.execute(INSERT_USER_RETURN_ID, (username, password))
                user_id = cursor.fetchone()["id"]
            except Exception as e:
                return jsonify({"error": "Username already exists.", "details": str(e)}), 409

    return jsonify({"id": user_id, "message": f"User {username} created successfully."}), 201


@users_bp.route("/api/user/login", methods=["POST"])
def login_user():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
            user = cursor.fetchone()

    if not user or user["password"] != password:
        return jsonify({"Login failed"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user["id"]
    }), 200


@users_bp.route("/api/user/<uuid:user_id>", methods=["PATCH"])
def update_user(user_id):

    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")
    if not new_username and not new_password:
        return jsonify({"error": "At least one field (username or password) must be provided."}), 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET username = COALESCE(%s, username), 
                    password = COALESCE(%s, password) 
                WHERE id = %s 
                RETURNING id, username;
            """, (new_username, new_password, str(user_id)))
            user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({
        "message": "User updated successfully.",
        "user_id": user["id"],
    }), 200


@users_bp.route("/api/user/<uuid:user_id>", methods=["DELETE"])
def delete_user(user_id):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (str(user_id),))
            deleted_user = cursor.fetchone()

    if not deleted_user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({
        "message": "User deleted successfully.",
        "user_id": deleted_user["id"]
    }), 200
