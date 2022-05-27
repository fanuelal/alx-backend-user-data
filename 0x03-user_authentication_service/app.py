#!/usr/bin/env python3
"""Module flask"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """json payload of the from"""
    jsn = jsonify({"message": "Bienvenue"})
    return jsn


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
