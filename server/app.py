"""
phone-cluster: server.app

Minimal Flask server for the Phone Cluster project.
"""

from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app
