from app.agents.base import GroqAgent
from app.models.schemas import Offer, NegotiationState
class BuyerAgent(GroqAgent):
    def __init__(self): super().__init__("buyer negotiation agent")
    def propose(self,state:NegotiationState)->Offer:
        s,b=state.seller,state.buyer
        last=next((o for o in reversed(state.offers) if o.actor=="seller"),None)
        instruction=(
          f"Return keys price_per_kg, quantity_kg, decision, rationale. "
          f"Buyer ceiling={b.max_price}; needs={b.quantity_kg}; seller floor={s.min_price}; "
          f"last seller offer={last.price_per_kg if last else 'none'}. "
          "Never exceed ceiling. Accept a valid seller offer at/below ceiling. Rationale under 20 words."
        )
        return Offer(actor="buyer",**self.json_call(instruction))
