"""
phone-cluster: server.app

Minimal Flask server for the Phone Cluster project.
"""

from flask import Flask, jsonify, request
from uuid import uuid4
from datetime import datetime, timezone


def create_app():
    app = Flask(__name__)

    # In-memory client registry (v0.x). Will move to persistence later.
    clients = {}

    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/ping")
    def ping():
        """
        Basic client → server contact endpoint.

        Expects JSON:
            {
              "client_name": "string"
            }

        Returns:
            {
              "received": true,
              "client": "string | null"
            }
        """
        if not request.is_json:
            return jsonify(
                received=False,
                error="Expected JSON body"
            ), 400

        data = request.get_json(silent=True) or {}
        client_name = data.get("client_name")

        return jsonify(
            received=True,
            client=client_name
        )

    return app
