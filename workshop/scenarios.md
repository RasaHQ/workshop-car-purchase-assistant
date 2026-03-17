# Workshop Scenarios

## Scenario 1: End-to-End Happy Path
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

## Scenario 2: Inventory Constraint and Recovery
Objective: show graceful fallback and decision framing.

Prompt sequence:
1. "Find me a used Honda Civic."
2. If no availability, ask: "Show similar options and the best dealer price."

Expected checks:
1. Assistant communicates no-match clearly when applicable.
2. Similar car/dealer recommendation path activates.
3. User is guided toward a concrete next decision.

## Scenario 3: Mid-Flow Requirement Change
Objective: test orchestration resilience and context updates.

Prompt sequence:
1. Start with a sedan search.
2. Midway switch to EV under a tighter budget.
3. Continue to financing and appointment.

Expected checks:
1. Updated requirements are reflected in later steps.
2. No stale recommendations are presented as final.
3. Final response includes coherent rationale.

## Optional Reliability Drill
Objective: incident-style diagnosis.

Inject one issue:
1. Port conflict on 5432.
2. Missing model artifact.
3. Startup race between app and Postgres.

Expected checks:
1. Team identifies root cause quickly from logs.
2. Team applies correct runbook command.
3. Team verifies recovery with service health and test prompt.

## Ambiguous Decision Cards (Questions Only)
Use these during the MCP vs A2A decision lab.

1. Need dealer recommendations, affordability pre-check, and then an immediate reservation suggestion in one continuous conversation.

2. Need recall lookup, safety ratings, and test-drive booking handled in a single customer journey.

3. Need a negotiation-style assistant that iterates across budget, trim, and dealer distance over multiple turns before final car selection.
