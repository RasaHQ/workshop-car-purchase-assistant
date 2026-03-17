#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "[error] docker is not installed or not in PATH"
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "[info] .env not found; creating from .env_example"
  cp .env_example .env
fi

if ! grep -q '^MOCK_TAVILY_SEARCH=' .env; then
  echo "[info] setting MOCK_TAVILY_SEARCH=true for workshop stability"
  echo "MOCK_TAVILY_SEARCH=true" >> .env
fi

echo "[step] stopping existing stack"
docker compose down --remove-orphans

echo "[step] training rasa model"
docker compose run --rm agentic_assistant train

echo "[step] starting workshop stack"
docker compose up -d --build

echo "[step] service status"
docker compose ps

echo "[done] workshop stack is up"
echo "[next] run scripts/workshop_verify.sh to validate endpoints"
