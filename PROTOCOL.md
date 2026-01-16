## v0.1 Protocol

### GET /health
Purpose: check if server is alive

Response:
{
  "status": "ok"
}

### POST /ping
Purpose: basic client → server contact

Request:
{
  "client_name": "string"
}

Response:
{
  "received": true
}
