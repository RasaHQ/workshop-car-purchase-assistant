# Facilitator Checklist and Rubric

## Delivery Checklist
1. Confirm all participants have Docker running.
2. Confirm `.env` exists and workshop mode is set as needed.
3. Confirm model was trained before `docker compose up`.
4. Confirm participants can access assistant endpoint.
5. Time-box each section strictly.

## Technical Verification Checklist
1. Services are up (`agentic_assistant`, `rasa_server`, MCP servers, A2A server, tracker store).
2. One full scenario runs without fatal errors.
3. Logs show at least one MCP call and one A2A call.
4. Tracker store persists events successfully.

## Assessment Rubric (0-2 each, 10 total)
1. Architecture clarity
- 0: Cannot explain component roles
- 1: Partial explanation
- 2: Clear MCP/A2A/orchestrator explanation

2. Decision quality (MCP vs A2A)
- 0: Repeated misclassification
- 1: Mixed correctness
- 2: Correct with sound justification

3. Hands-on modification
- 0: No successful change
- 1: Change made but unverified
- 2: Change made and verified end-to-end

4. Debugging effectiveness
- 0: Could not isolate root cause
- 1: Isolated cause with heavy assistance
- 2: Isolated and fixed independently

5. Customer-facing articulation
- 0: No clear business framing
- 1: Technical framing only
- 2: Ties architecture choices to customer outcomes and risk

## Debrief Questions
1. What customer signals indicate MCP is enough?
2. What signals indicate A2A is required?
3. Where did orchestration add the most value?
4. What would you change before production rollout?

## Pass/Follow-Up Guidance
1. 8-10: Ready to lead customer design discussions.
2. 5-7: Ready with coaching on decision framing.
3. 0-4: Repeat workshop with focus on architecture and debugging labs.
