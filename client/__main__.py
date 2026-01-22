"""
phone-cluster: client.__main__

Module entrypoint for running the Phone Cluster client.
"""

import os
from pathlib import Path

import requests
import tomllib

CONFIG_DIR = Path.home() / ".config" / "phone-cluster"
CONFIG_FILE = CONFIG_DIR / "client.toml"


def load_client_config():
    """
    Load client configuration from TOML if present.

    Precedence:
      1. Environment variables
      2. TOML config file
      3. Defaults
    """
    config = {
        "server_url": "http://127.0.0.1:8787",
        "client_name": "example-client",
        "client_id": None,
    }

    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("rb") as f:
                data = tomllib.load(f)
            client_cfg = data.get("client", {})
            config.update(client_cfg)
        except Exception as exc:
            print(f"Warning: failed to read config file: {exc}")

    config["server_url"] = os.getenv("PHONE_CLUSTER_URL", config["server_url"])
    config["client_name"] = os.getenv("PHONE_CLUSTER_CLIENT_NAME", config["client_name"])

    return config


def save_client_id(client_id: str) -> None:
    """
    Save client_id to ~/.config/phone-cluster/client.toml.

    This does not overwrite the file if it already contains a client_id.
    It will create the directory/file if missing.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Minimal TOML writer for our small config surface (v0.x).
    # We only ensure [client] and client_id exist.
    if CONFIG_FILE.exists():
        text = CONFIG_FILE.read_text(encoding="utf-8")
    else:
        text = ""

    if "client_id" in text:
        # Don't overwrite an existing client_id.
        return

    if "[client]" not in text:
        if text and not text.endswith("\n"):
            text += "\n"
        text += "[client]\n"

    # Ensure file ends with newline before appending
    if text and not text.endswith("\n"):
        text += "\n"
    text += f'client_id = "{client_id}"\n'

    CONFIG_FILE.write_text(text, encoding="utf-8")

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
