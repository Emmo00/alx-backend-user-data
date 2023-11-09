#!/usr/bin/env python3
"""view for Session Authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """session login route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    User.load_from_file()
    result = User.search({'email': email})
    if not result or len(result) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = result[0]
    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    return abort(404)
