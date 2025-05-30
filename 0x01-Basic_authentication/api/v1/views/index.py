>#!/usr/bin/env python3
""" Module of Index views
"""
from flask import abort, jsonify

from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats/", strict_slashes=False)
def stats() -> str:
    """GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User

    api_stats = {"users": User.count()}
    return jsonify(api_stats)


@app_views.route("/unauthorized", methods=["GET"], strict_slashes=False)
def unauthorized() -> None:
    """GET /api/v1/unauthorized

    Returns:
        Error 401 with a message stating why the error was returned.
    """
    abort(401)


@app_views.route("/forbidden", methods=["GET"], strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/forbidden

    Returns:
        Error 401 with a message stating why the error was returned.
    """
    abort(403)
