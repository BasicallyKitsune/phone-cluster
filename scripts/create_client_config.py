"""
Create and inspect the Phone Cluster client TOML config.

- Ensures the config directory exists
- Creates a default client.toml if missing
- Loads and prints the resolved configuration

Development helper only.
"""

import os
from pathlib import Path
import tomllib


CONFIG_DIR = Path.home() / ".config" / "phone-cluster"
CONFIG_FILE = CONFIG_DIR / "client.toml"


DEFAULT_CONFIG = """\
# Phone Cluster - Client Configuration

[client]
server_url = "http://127.0.0.1:8787"
client_name = "example-client"
"""


def ensure_config_exists():
    if CONFIG_FILE.exists():
        return

    print(f"Creating default config at: {CONFIG_FILE}")
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(DEFAULT_CONFIG, encoding="utf-8")


def load_client_config():
    config = {
        "server_url": "http://127.0.0.1:8787",
        "client_name": "example-client",
    }

    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("rb") as f:
            data = tomllib.load(f)
        client_cfg = data.get("client", {})
        config.update(client_cfg)

    config["server_url"] = os.getenv(
        "PHONE_CLUSTER_URL",
        config["server_url"]
    )
    config["client_name"] = os.getenv(
        "PHONE_CLUSTER_CLIENT_NAME",
        config["client_name"]
    )

    return config


if __name__ == "__main__":
    ensure_config_exists()
    cfg = load_client_config()

    print("Resolved client configuration:")
    print(f"  server_url : {cfg['server_url']}")
    print(f"  client_name: {cfg['client_name']}")
