# Customer Success Engineering Workshop (Offsite Spring 2026): MCP, A2A, and Orchestration

## Learning Outcomes
By the end of this workshop, participants can:
1. Explain the roles of orchestration, MCP servers, and A2A agents.
2. Decide when to use MCP vs A2A for a customer requirement.
3. Apply a small but meaningful change safely and validate end-to-end behavior.
4. Diagnose common runtime issues (model missing, port conflict, startup race, stream errors).

## Repo Architecture
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
1. Get the .env from 1Password shared file and use it in the repo.

2. Start services bu running:
```bash
./scripts/workshop_start.sh 
```

3. Verify everything works:
```bash
./scripts/workshop_verify.sh 
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

## Lab Exercise
# Workshop Scenarios

## End-to-End Happy Path Example
Objective: trace orchestration across all phases.

Prompt sequence:
1. "I need a reliable compact SUV under $35k."
2. "Find one at a dealer near me."
3. "Can I afford this with a 72-month loan?"
4. "Book me an appointment next Tuesday afternoon."

Expected checks:
1. MCP search is used for research.
2. A2A shopping agent is used for dealer/car decisioning.
3. Financing flow runs in main orchestrator context.
4. MCP appointment tool is called for scheduling.

## Ambiguous Decision Scenarios
1. Cross-Agent handoff policy when one agent is active

* User: I’m looking for a reliable used sedan under $25,000.
* Assistant: I can help with that. Do you have a preferred model or dealer?
* User: Show me options near me.
* Assistant: I found a 2023 Mazda3 at Budget Cars Plus for $22,000. Would you like to reserve it?
* User: Can I afford this with a 72-month loan and $5,000 down?
* Assistant: Sure, I’ll check affordability. What are your monthly income and monthly expenses?
* User: Income is $9,000 and expenses are $3,200.
* Assistant: Based on your finances, here’s your affordability assessment and estimated monthly payment range.
* Assistant: Returning to your selected car: the 2023 Mazda3 at Budget Cars Plus for $22,000.
* Assistant: Would you like to proceed with reserving it?
* User: Yes, reserve it.
* Assistant: Done. I’ve recorded your reservation decision for the 2023 Mazda3 at Budget Cars Plus.
* User: Great, now book a test-drive appointment next Tuesday afternoon.
* Assistant: I found available slots and booked your appointment for next Tuesday afternoon.

2. Need dealer recommendations, affordability pre-check, and then an immediate reservation suggestion in one continuous conversation.

* User: I’m looking for a compact SUV under $35k. Can you recommend dealers that have good options nearby?
* Assistant: I can help with that. Are you looking for a new or used compact SUV, and what matters most to you: price, safety, features, or dealer distance?
* User: New. Safety and dealer distance matter most.
* Assistant: Do you have a preferred trim level, and what’s the maximum distance you want to travel to a dealer?
* User: Premium trim if possible, and no more than 15 miles.
* Assistant: I found a few dealer options that match your preferences. The best match is the 2024 Subaru Forester at Family Auto Hub for $31,000. It has a high safety score and the dealer is only 9 miles away. Would you like me to check whether this fits your budget before we reserve it?
* User: Yes. Check if I can afford it with a 72-month loan and $5k down.
* Assistant: I’ll help with that. What is your monthly gross income before taxes?
* User: 15000
* Assistant: What are your estimated monthly expenses excluding existing debt payments?
* User: 5000
* Assistant: Based on your monthly income of $15000 and monthly expenses of $5000, your debt-to-income ratio is healthy enough for this loan scenario. Do you want to continue with the 2024 Subaru Forester at Family Auto Hub?
* User: Yes, reserve it.
* Assistant: Done. I’ve recorded your reservation request for the 2024 Subaru Forester at Family Auto Hub for $31,000.