"""
phone-cluster: server.app

Minimal Flask server for the Phone Cluster project.
"""

from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

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
