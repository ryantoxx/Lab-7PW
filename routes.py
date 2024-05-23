from flask import request, jsonify
from models.database import db
from models.recipes import Recipe
from __main__ import app
from app import authenticate
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

def admin_required(fn):
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return jsonify({"error": "Admin access required"}), 401
        return fn(*args, **kwargs)
    return wrapper

# TOKEN CREATION
@app.route('/api/token', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username and password:
        if authenticate(username, password):
            access_token = create_access_token(identity=username)
            return jsonify({'Bearer': access_token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return jsonify({'error': 'Username and password required'}), 400

