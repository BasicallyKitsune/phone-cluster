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

    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def row_to_client(row):
        return {
            "client_id": row["client_id"],
            "name": row["name"],
            "created_at": row["created_at"],
            "last_seen": row["last_seen"],
            "capabilities": json.loads(row["capabilities"] or "{}"),
        }


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

        client_id = str(__import__("uuid").uuid4())
        created_at = dbmod.now_iso()

        capabilities = data.get("capabilities")
        if not isinstance(capabilities, dict):
            capabilities = {}

        conn = get_db()
        conn.execute(
            """
            INSERT INTO clients (client_id, name, created_at, last_seen, capabilities)
            VALUES (?, ?, ?, ?, ?)
            """,
            (client_id, name.strip(), created_at, created_at, json.dumps(capabilities)),
        )
        conn.commit()

        return jsonify(client_id=client_id), 201


    @app.get("/v1/clients")
    def list_clients():
        conn = get_db()
        rows = conn.execute(
            "SELECT client_id, name, created_at, last_seen, capabilities FROM clients ORDER BY created_at DESC"
        ).fetchall()
        return jsonify(clients=[row_to_client(r) for r in rows])


    @app.get("/v1/clients/<client_id>")
    def get_client(client_id: str):
        conn = get_db()
        row = conn.execute(
            "SELECT client_id, name, created_at, last_seen, capabilities FROM clients WHERE client_id = ?",
            (client_id,),
        ).fetchone()

        if row is None:
            return jsonify(error="Client not found"), 404

        return jsonify(row_to_client(row))


    @app.post("/v1/heartbeat")
    def heartbeat():
        if not request.is_json:
            return jsonify(error="Expected JSON body"), 400

        data = request.get_json(silent=True) or {}
        client_id = data.get("client_id")

        if not isinstance(client_id, str) or not client_id.strip():
            return jsonify(error="Missing or invalid 'client_id'"), 400

        conn = get_db()
        cur = conn.execute(
            "UPDATE clients SET last_seen = ? WHERE client_id = ?",
            (dbmod.now_iso(), client_id.strip()),
        )
        conn.commit()

        if cur.rowcount == 0:
            return jsonify(error="Client not found"), 404

        return jsonify(ok=True)


    return app
