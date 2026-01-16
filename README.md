# 🌸 Phone Cluster

My lightweight, cozy little server–client system for experimenting with a phone-based cluster.

## What is this?

This project is a tiny server + client setup designed for:
- phones running Termux
- mixed environments (Arch / Ubuntu / Android)

This is v0.1 so I'm not including many features.

## Project layout

server/ # Flask-based server
client/ # Simple HTTP client
clusterctl/ # Install / uninstall manager
scripts/ # Thin shell wrappers
config/ # Example config files

## Versioning & scope

v0.1 goals
 - install / uninstall works
 - server responds to a health check
 - client can contact server
 - paths and config format are locked in