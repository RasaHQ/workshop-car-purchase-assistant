from rasa.agents.protocol.a2a.a2a_agent import A2AAgent
from rasa.agents.schemas import AgentInput, AgentOutput

from typing import Any, Dict, List, Optional
from rasa.agents.schemas.agent_input import AgentInputSlot
from rasa.shared.core.events import SlotSet

REQUIRED_FINAL_DECISION_FIELDS = ("final_decision", "car_model", "dealer_name", "price")


class CarShoppingAgent(A2AAgent):

    async def process_input(self, input: AgentInput) -> AgentInput:
        """Pre-process the input before sending it to Rasa."""
        slots_to_keep: List[AgentInputSlot] = []
        for slot in input.slots:
            if slot.name == "recommended_car_models":
                slots_to_keep.append(slot)
            if slot.name == "recommended_car_details":
                slots_to_keep.append(slot)

        input.slots = slots_to_keep
        return input

    @staticmethod
    def _extract_final_decision(result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract final decision payload from one structured result item."""
        result_payload = result.get("result", {})
        if not isinstance(result_payload, dict):
            return None
        final_decision = result_payload.get("final_reservation_decision")
        if not isinstance(final_decision, dict):
            return None
        return final_decision

    async def process_agent_output(self, output: AgentOutput) -> AgentOutput:
        """Post-process the output before returning it to Rasa.

        Example of structured_results:
        structured_results=[
          [{
            'name': 'shopping_agent_1',
            'result': {
              'final_reservation_decision': {
                'final_decision': 'reserve',
                'car_model': '2020 Audi Q3',
                'dealer_name': 'Premium Auto Center',
                'price': 23500
            },
          }]
        ]
        """
        tool_results = output.structured_results

        slot_events: List[SlotSet] = []

        if not tool_results:
            return output

        for index in range(len(tool_results)):
            iteration_results = tool_results[index]
            for result in iteration_results:
                final_decision = self._extract_final_decision(result)
                if not final_decision:
                    continue

                # Enforce contract shape: ignore malformed results to avoid corrupt slot state.
                if any(field not in final_decision for field in REQUIRED_FINAL_DECISION_FIELDS):
                    continue

                if final_decision.get("final_decision") != "reserve":
                    continue

                slot_events.append(SlotSet("car_model", final_decision.get("car_model")))
                slot_events.append(SlotSet("car_price", final_decision.get("price")))
                slot_events.append(SlotSet("dealer_name", final_decision.get("dealer_name")))

        # add the slot events to the output
        if slot_events:
            if not output.events:
                output.events = slot_events
            else:
                output.events.extend(slot_events)
        return output
