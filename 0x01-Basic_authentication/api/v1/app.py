#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Dict, Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()
elif auth_type == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()


@app.errorhandler(404)
def not_found(_) -> Tuple[Dict, int]:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(_) -> Tuple[Dict, int]:
    """Unauthorized error handler."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(_) -> Tuple[Dict, int]:
    """Forbidden API operation handler."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Before request handler."""
    if auth is None:
        return

    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if not auth.authorization_header(request):
        abort(401)

    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=getenv("DEBUG", False))
