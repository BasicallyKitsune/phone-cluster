"""
phone-cluster: server.app

Minimal Flask server for the Phone Cluster project.
"""

import json
from pathlib import Path

from flask import Flask, jsonify, request, g
from uuid import uuid4
from datetime import datetime, timezone

from server import db as dbmod


def create_app():
    app = Flask(__name__)

    # In-memory client registry (v0.x). Will move to persistence later.
    clients = {}

    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    # Create one DB connection per request (stored in flask.g)
    def get_db():
        conn = g.get("db_conn")
        if conn is None:
            conn = dbmod.connect()
            dbmod.init_db(conn)
            g.db_conn = conn
        return conn

    @app.teardown_appcontext
    def close_db(_exc):
        conn = g.pop("db_conn", None)
        if conn is not None:
            conn.close()

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

    @app.get("/v1/clients")
    def list_clients():
        return jsonify(clients=list(clients.values()))

    @app.get("/v1/clients/<client_id>")
    def get_client(client_id: str):
        client = clients.get(client_id)
        if client is None:
            return jsonify(error="Client not found"), 404
        return jsonify(client)

    @app.post("/v1/heartbeat")
    def heartbeat():
        if not request.is_json:
            return jsonify(error="Expected JSON body"), 400

        data = request.get_json(silent=True) or {}
        client_id = data.get("client_id")

        if not isinstance(client_id, str) or not client_id.strip():
            return jsonify(error="Missing or invalid 'client_id'"), 400

        client = clients.get(client_id)
        if client is None:
            return jsonify(error="Client not found"), 404

        client["last_seen"] = now_iso()
        return jsonify(ok=True)

    return app
