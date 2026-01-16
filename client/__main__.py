"""
phone-cluster: client.__main__

Module entrypoint for running the Phone Cluster client.
"""

import os
from pathlib import Path

import requests
import tomllib

def load_client_config():
    """
    Load client configuration from TOML if present.

    Precedence:
      1. Environment variables
      2. TOML config file
      3. Defaults
    """
    # Defaults
    config = {
        "server_url": "http://127.0.0.1:8787",
        "client_name": "example-client",
    }

    # TOML config (optional)
    config_path = Path.home() / ".config" / "phone-cluster" / "client.toml"
    if config_path.exists():
        try:
            with config_path.open("rb") as f:
                data = tomllib.load(f)
            client_cfg = data.get("client", {})
            config.update(client_cfg)
        except Exception as exc:
            print(f"Warning: failed to read config file: {exc}")

    # Environment overrides
    config["server_url"] = os.getenv(
        "PHONE_CLUSTER_URL",
        config["server_url"],
    )
    config["client_name"] = os.getenv(
        "PHONE_CLUSTER_CLIENT_NAME",
        config["client_name"],
    )

    return config


def main():
    cfg = load_client_config()
    base_url = cfg["server_url"]

    # ---- health check ----
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        response.raise_for_status()
        print("Health check response:", response.json())
    except Exception as exc:
        print("Failed to contact server:", exc)
        return  # no point continuing if server is down

    # ---- ping ----
    payload = {
        "client_name": cfg["client_name"],
    }

    try:
        response = requests.post(
            f"{base_url}/ping",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        print("Ping response:", response.json())
    except Exception as exc:
        print("Ping failed:", exc)


if __name__ == "__main__":
    main()
