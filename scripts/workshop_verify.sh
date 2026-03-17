#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "[error] $1"
  exit 1
}

echo "[step] checking docker daemon"
docker info >/dev/null 2>&1 || fail "docker daemon not reachable"

echo "[step] checking compose services"
docker compose ps

echo "[step] checking model artifact"
ls models/*.tar.gz >/dev/null 2>&1 || fail "no trained model found in models/"

echo "[step] checking assistant endpoints"
curl -fsS http://localhost:5005 >/dev/null || fail "assistant endpoint http://localhost:5005 not reachable"
curl -fsS http://localhost:5006 >/dev/null || fail "rasa server endpoint http://localhost:5006 not reachable"

echo "[step] checking critical logs for fatal errors"
LOGS="$(docker compose logs --tail=120 agentic_assistant rasa_server tracker_store 2>/dev/null || true)"
if echo "$LOGS" | rg -q "(Traceback|failed to set up container networking|could not translate host name|The provided model path 'models' could not be found)"; then
  echo "[warn] potential errors detected in recent logs; inspect with:"
  echo "       docker compose logs --tail=200 agentic_assistant rasa_server tracker_store"
else
  echo "[ok] no critical known errors found in recent logs"
fi

echo "[done] workshop verification complete"
