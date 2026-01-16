"""
phone-cluster: client.__main__

Module entrypoint for running the Phone Cluster client.
"""

def main():
    import requests

    url = "http://127.0.0.1:8787/health"

    try:
        r = requests.get(url, timeout=5)
        print("Server response:", r.json())
    except Exception as e:
        print("Failed to contact server:", e)


if __name__ == "__main__":
    main()
