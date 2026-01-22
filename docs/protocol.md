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
client_id = "string | null"
```

Environment variables:

* PHONE_CLUSTER_URL
* PHONE_CLUSTER_CLIENT_NAME

Defaults:

* server_url: [http://127.0.0.1:8787](http://127.0.0.1:8787)
* client_name: example-client
* client_id: null

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

---

### POST /v1/register

Purpose: register a client and assign a stable client_id.

Request:

```json
{
  "name": "string"
}
```

Response:

```json
{
  "client_id": "string"
}
```

---

### POST /v1/heartbeat

Purpose: report client liveness.

Request:

```json
{
  "client_id": "string"
}
```

Response:

```json
{
  "ok": true
}
```

---

### GET /v1/clients

Purpose: list registered clients.

Response:

```json
{
  "clients": [
    {
      "client_id": "string",
      "name": "string",
      "created_at": "iso8601",
      "last_seen": "iso8601",
      "capabilities": {}
    }
  ]
}
```

---

### GET /v1/clients/{client_id}

Purpose: retrieve a single client record.

Response:

```json
{
  "client_id": "string",
  "name": "string",
  "created_at": "iso8601",
  "last_seen": "iso8601",
  "capabilities": {}
}
```
