#!/usr/bin/env python3
""" Route module for the API """
from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /  JSON payload"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ 
    Registers new user with email and pswd in x-www-form-urlencoded request
    """
    form_data = request.form

    if "email" not in form_data:
        return jsonify({"message": "email required"}), 400
    elif "password" not in form_data:
        return jsonify({"message": "password required"}), 400
    else:

        email = request.form.get("email")
        pswd = request.form.get("password")

        try:
            new_user = AUTH.register_user(email, pswd)
            return jsonify({
                "email": new_user.email,
                "message": "user created"
            })
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ 
    Creates new session for user, stores as cookie
    """
    form_data = request.form

    if "email" not in form_data:
        return jsonify({"message": "email required"}), 400
    elif "password" not in form_data:
        return jsonify({"message": "password required"}), 400
    else:

        email = request.form.get("email")
        pswd = request.form.get("password")

        if AUTH.valid_login(email, pswd) is False:
            abort(401)
        else:
            session_id = AUTH.create_session(email)
            response = jsonify({
                "email": email,
                "message": "logged in"
                })
            response.set_cookie('session_id', session_id)

            return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """ 
      Redirects user to status route (GET /)
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ 
    Finds user's info by finding session_id (key in cookie)
   
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                return jsonify({"email": user.email}), 200
            else:
                abort(403)
        except NoResultFound:
            abort(403)
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ 
    Generates pswd reset token
    """
    form_data = request.form

    if "email" not in form_data:
        return jsonify({"message": "email required"}), 400
    else:

        email = request.form.get("email")

        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({
                "email": email,
                "reset_token": reset_token
            }), 200
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ PUT /reset_password
    Updates user password - JSON payload
    """
    form_data = request.form

    if "email" not in form_data:
        return jsonify({"message": "email required"}), 400
    if "reset_token" not in form_data:
        return jsonify({"message": "reset_token required"}), 400
    if "new_password" not in form_data:
        return jsonify({"message": "new_password required"}), 400
    else:

        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_pswd = request.form.get("new_password")

        try:
            AUTH.update_password(reset_token, new_pswd)
            return jsonify({
                "email": email,
                "message": "Password updated"
            }), 200
        except ValueError:
            abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
