## v0.1 Protocol

This document describes the API endpoints and configuration used in
Phone Cluster v0.1.

---

## Configuration

Configuration precedence is:

Environment variables → TOML files → Defaults

---

### Client Configuration

TOML file:

```
~/.config/phone-cluster/client.toml
```

Format:

```toml
[client]
server_url = "http://127.0.0.1:8787"
client_name = "example-client"
```

Environment variables:

* PHONE_CLUSTER_URL
* PHONE_CLUSTER_CLIENT_NAME

Defaults:

* server_url: [http://127.0.0.1:8787](http://127.0.0.1:8787)
* client_name: example-client

---

### Server Configuration

TOML file:

```
~/.config/phone-cluster/server.toml
```

Format:

```toml
[server]
host = "0.0.0.0"
port = 8787
```

Environment variables:

* PHONE_CLUSTER_HOST
* PHONE_CLUSTER_PORT

Defaults:

* host: 0.0.0.0
* port: 8787

---

## API Endpoints

### GET /health

Purpose: check if server is running.

Response:

```json
{
  "status": "ok"
}
```

---

### POST /ping

Purpose: basic client to server contact.

Request:

```json
{
  "client_name": "string"
}
```

Response:

```json
{
  "received": true,
  "client": "string | null"
}
```
