"""
phone-cluster: client.__main__

Module entrypoint for running the Phone Cluster client.
"""

def main():
    import requests

    base_url = "http://127.0.0.1:8787"

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
        "client_name": "test-client"
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
