"""
Create and inspect the Phone Cluster TOML configs.

- Ensures the config directory exists
- Creates default client.toml and server.toml if missing
- Loads and prints the resolved configuration values

Development helper only.
"""

import os
from pathlib import Path
import tomllib


CONFIG_DIR = Path.home() / ".config" / "phone-cluster"
CLIENT_CONFIG_FILE = CONFIG_DIR / "client.toml"
SERVER_CONFIG_FILE = CONFIG_DIR / "server.toml"


DEFAULT_CLIENT_CONFIG = """\
# Phone Cluster - Client Configuration

[client]
server_url = "http://127.0.0.1:8787"
client_name = "example-client"
"""

DEFAULT_SERVER_CONFIG = """\
# Phone Cluster - Server Configuration

[server]
host = "0.0.0.0"
port = 8787
"""


def ensure_configs_exist() -> None:
    """Create default client/server config files if they do not exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CLIENT_CONFIG_FILE.exists():
        print(f"Creating default client config at: {CLIENT_CONFIG_FILE}")
        CLIENT_CONFIG_FILE.write_text(DEFAULT_CLIENT_CONFIG, encoding="utf-8")

    if not SERVER_CONFIG_FILE.exists():
        print(f"Creating default server config at: {SERVER_CONFIG_FILE}")
        SERVER_CONFIG_FILE.write_text(DEFAULT_SERVER_CONFIG, encoding="utf-8")


def load_client_config() -> dict:
    """Load client config with precedence: env > toml > defaults."""
    config = {
        "server_url": "http://127.0.0.1:8787",
        "client_name": "example-client",
    }

    if CLIENT_CONFIG_FILE.exists():
        with CLIENT_CONFIG_FILE.open("rb") as f:
            data = tomllib.load(f)
        config.update(data.get("client", {}))

    config["server_url"] = os.getenv("PHONE_CLUSTER_URL", config["server_url"])
    config["client_name"] = os.getenv("PHONE_CLUSTER_CLIENT_NAME", config["client_name"])
    return config


def load_server_config() -> dict:
    """Load server config with precedence: env > toml > defaults."""
    config = {
        "host": "0.0.0.0",
        "port": 8787,
    }

    if SERVER_CONFIG_FILE.exists():
        with SERVER_CONFIG_FILE.open("rb") as f:
            data = tomllib.load(f)
        config.update(data.get("server", {}))

    config["host"] = os.getenv("PHONE_CLUSTER_HOST", config["host"])
    config["port"] = int(os.getenv("PHONE_CLUSTER_PORT", str(config["port"])))
    return config


if __name__ == "__main__":
    ensure_configs_exist()

    client_cfg = load_client_config()
    server_cfg = load_server_config()

    print("Resolved client configuration:")
    print(f"  server_url : {client_cfg['server_url']}")
    print(f"  client_name: {client_cfg['client_name']}")
    print()

    print("Resolved server configuration:")
    print(f"  host: {server_cfg['host']}")
    print(f"  port: {server_cfg['port']}")
