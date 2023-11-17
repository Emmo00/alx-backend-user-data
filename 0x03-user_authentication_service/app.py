#!/usr/bin/env python3
"""simple flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def root():
    """root route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """register user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        return abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({'emaill': email, 'message': 'logged in'})
    res.set_cookie('session_id', session_id)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    return abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
