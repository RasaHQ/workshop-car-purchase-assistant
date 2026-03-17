# State Contract Design: Orchestration Continuity

This document defines the state handoff contract between the shopping A2A agent and the Rasa orchestration layer.

## Why this contract exists
When a specialist agent (A2A) returns data to the orchestrator, downstream routing and resume behavior depend on stable fields. If payload shape drifts, handoffs fail silently and cross-flow continuity degrades.

## Contract: `final_reservation_decision`

Version: `shopping-a2a-v1`

Required fields:
1. `final_decision` (`reserve` or `decline`)
2. `car_model` (string)
3. `dealer_name` (string)
4. `price` (number)

Optional fields:
1. `user_response`
2. `decision_timestamp`

## Orchestrator slot mapping
When `final_decision == reserve`, the orchestrator maps:
1. `car_model` -> slot `car_model`
2. `dealer_name` -> slot `dealer_name`
3. `price` -> slot `car_price`

## Enforcement points in this repo
1. Producer (A2A server):
- `servers/car_shopping_server/agent_executor.py`
- Emits `state_contract` metadata and `final_reservation_decision` payload.

2. Consumer (orchestrator wrapper):
- `custom/car_shopping_agent.py`
- Validates required fields before applying slot events.

## Design guidance for customers
1. Version every contract payload (`state_contract.version`).
2. Keep required fields minimal and stable.
3. Validate contracts before mutating orchestrator state.
4. Add optional fields without breaking required core fields.
5. Treat missing required fields as non-fatal and continue conversation safely.
