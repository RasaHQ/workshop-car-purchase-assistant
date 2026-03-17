# Workshop Troubleshooting Runbook

This runbook covers the most common setup failures observed in this project.

## 1) Port 5432 Already Allocated

Symptom:
- `Bind for 0.0.0.0:5432 failed: port is already allocated`

Diagnosis:
```bash
lsof -nP -iTCP:5432 -sTCP:LISTEN
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | rg 5432
```

Fix:
1. Stop current project stack:
```bash
docker compose down --remove-orphans
```
2. Stop/remove the conflicting container (example from workshop):
```bash
docker stop rasa_postgres
docker rm rasa_postgres
```
3. Start again:
```bash
docker compose up
```

Notes:
- Do not kill Docker Desktop process directly to free ports.
- If local Postgres service is using 5432, stop it with `brew services stop postgresql` (or matching versioned service).

## 2) Docker Daemon Unavailable

Symptom:
- `Cannot connect to the Docker daemon at unix:///.../docker.sock`

Fix:
1. Start/restart Docker Desktop.
2. Verify daemon is reachable:
```bash
docker info
```
3. Retry your compose command.

## 3) Missing Rasa Model

Symptom:
- `The provided model path 'models' could not be found`

Fix:
1. Train model before running stack:
```bash
docker compose run --rm agentic_assistant train
```
2. Verify model artifact exists:
```bash
ls -la models
```
3. Bring up services:
```bash
docker compose up
```

## 4) Postgres Startup Race / Temporary DNS Failure

Symptom:
- Intermittent startup errors like:
  - `could not translate host name "tracker_store"`
  - followed by eventual successful connection

Status in this repo:
- `docker-compose.yml` includes a `tracker_store` healthcheck and dependency conditions so app services wait for DB readiness.

Recovery:
```bash
docker compose down --remove-orphans
docker compose up --build
```

## 5) `MOCK_TAVILY_SEARCH` Warning

Symptom:
- `The "MOCK_TAVILY_SEARCH" variable is not set. Defaulting to a blank string.`

Fix (recommended for workshops):
```bash
echo "MOCK_TAVILY_SEARCH=true" >> .env
```

## 6) Car Shopping Server Stream Noise (`GeneratorExit` / OpenTelemetry detach)

Symptom:
- Logs show `GeneratorExit` and context detach errors in `car_shopping_A2A_agent_server`.

Status in this repo:
- `servers/car_shopping_server/agent_executor.py` was updated to avoid closing async stream early.

Recovery after pulling latest changes:
```bash
docker compose up -d --build car_shopping_a2a_agent_server
```

## 7) Quick Health Commands

```bash
docker compose ps -a
docker compose logs --tail=120 agentic_assistant rasa_server tracker_store
```

## 8) Full Reset (Last Resort)

Use only if normal fixes fail:
```bash
docker compose down --remove-orphans
docker compose up --build
```

If still failing, capture and share:
1. `docker compose ps -a`
2. `docker compose logs --tail=200`
3. exact command used and full error output
