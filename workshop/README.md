# Customer Success Engineering Workshop: MCP, A2A, and Orchestration

## Audience
Professional Customer Success Engineers who need to scope, shape, and guide agentic solution designs with customers.

## Duration
90 minutes (hands-on)

## Learning Outcomes
By the end of this workshop, participants can:
1. Explain the roles of orchestration, MCP servers, and A2A agents in this repo.
2. Decide when to use MCP vs A2A for a customer requirement.
3. Apply a small but meaningful change safely and validate end-to-end behavior.
4. Diagnose common runtime issues (model missing, port conflict, startup race, stream errors).

## Repo Architecture Map (for teaching)
- Main orchestrator: `agentic_assistant` / `rasa_server`
- Docker wiring: `docker-compose.yml`
- Endpoints and tracker config: `endpoints-docker-compose.yml`
- MCP server (web search): `servers/tavily_search_server/`
- MCP server (appointment booking): `servers/appointment_booking_server/`
- A2A server (shopping): `servers/car_shopping_server/`
- Shopping A2A execution path:
  - Server: `servers/car_shopping_server/car_shopping_server.py`
  - Executor: `servers/car_shopping_server/agent_executor.py`
  - Agent/tools: `servers/car_shopping_server/agent.py`
  - Mock inventory: `servers/car_shopping_server/cars.json`

## Setup Instructions (for participants)
1. Copy env and set keys:
```bash
cp .env_example .env
```
2. Optional for workshop stability (recommended):
```bash
echo "MOCK_TAVILY_SEARCH=true" >> .env
```
3. Train model:
```bash
docker compose run --rm agentic_assistant train
```
4. Start services:
```bash
docker compose up
```

## Core Concept: MCP vs A2A vs Orchestration
1. MCP
- Use for tool-like capabilities with explicit schemas and predictable I/O.
- Good fit: search, booking query, deterministic lookups.

2. A2A
- Use when delegating to another autonomous specialist agent with its own lifecycle/state.
- Good fit: multi-step car shopping decisions and reservation workflow.

3. Orchestration
- Use for cross-step journey control, context continuity, and routing decisions.
- Good fit: deciding which specialist/tool to invoke next across the full customer journey.

## Decision Matrix
Use this quick matrix during customer discovery:

1. Is the need a single capability with clear inputs/outputs?
- Yes -> MCP
- No -> Continue

2. Is the need a specialist with multi-step autonomy and state?
- Yes -> A2A
- No -> Continue

3. Is the need coordination across multiple systems over time?
- Yes -> Orchestration layer

4. Is low latency and deterministic behavior critical?
- Prefer MCP first, then orchestrate.

5. Is explainability of agent decisions and handoff context critical?
- Prefer A2A + orchestration with structured artifacts/state.

## Lab Exercise
Detailed scenarios: `workshop/scenarios.md`

