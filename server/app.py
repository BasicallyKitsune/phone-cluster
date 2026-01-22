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

    @app.post("/v1/register")
    def register():
        if not request.is_json:
            return jsonify(error="Expected JSON body"), 400

        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not isinstance(name, str) or not name.strip():
            return jsonify(error="Missing or invalid 'name'"), 400

        client_id = str(uuid4())
        created_at = now_iso()

        clients[client_id] = {
            "client_id": client_id,
            "name": name.strip(),
            "created_at": created_at,
            "last_seen": created_at,
            "capabilities": data.get("capabilities") if isinstance(data.get("capabilities"), dict) else {},
        }

        return jsonify(client_id=client_id), 201

    return app
