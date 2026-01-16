"""
phone-cluster: server.__main__

Module entrypoint for running the Phone Cluster server.
"""

def main():
    from server.app import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=8787)


if __name__ == "__main__":
    main()
