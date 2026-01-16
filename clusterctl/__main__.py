"""
phone-cluster: clusterctl.__main__

Command-line entrypoint for managing Phone Cluster installs.
"""

import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: clusterctl <install|uninstall> <server|client>")
        sys.exit(1)

    command = sys.argv[1]
    role = sys.argv[2]

    if command == "install":
        print(f"[clusterctl] Installing {role} (not fully implemented yet)")
    elif command == "uninstall":
        print(f"[clusterctl] Uninstalling {role} (not fully implemented yet)")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
