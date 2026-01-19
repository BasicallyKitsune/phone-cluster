"""
phone-cluster: server.__main__

Module entrypoint for running the Phone Cluster server.
"""

import os
from pathlib import Path
import tomllib


def load_server_config():
    config = {
        "host": "0.0.0.0",
        "port": 8787,
    }

    config_path = Path.home() / ".config" / "phone-cluster" / "server.toml"
    if config_path.exists():
        try:
            with config_path.open("rb") as f:
                data = tomllib.load(f)
            server_cfg = data.get("server", {})
            config.update(server_cfg)
        except Exception as exc:
            print(f"Warning: failed to read {config_path}: {exc}")

    # Env overrides (highest precedence)
    config["host"] = os.getenv("PHONE_CLUSTER_HOST", config["host"])
    config["port"] = int(os.getenv("PHONE_CLUSTER_PORT", str(config["port"])))

    return config


def main():
    from server.app import create_app

    cfg = load_server_config()
    app = create_app()
    app.run(host=cfg["host"], port=cfg["port"])


if __name__ == "__main__":
    main()
