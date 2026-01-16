"""
phone-cluster: server.__main__

Module entrypoint for running the Phone Cluster server.
"""

import os

host = os.getenv("PHONE_CLUSTER_HOST", "0.0.0.0")
port = int(os.getenv("PHONE_CLUSTER_PORT", "8787"))

def main():
    from server.app import create_app

    app = create_app()
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
