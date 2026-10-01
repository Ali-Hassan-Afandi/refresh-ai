from app.agents.base import GroqAgent
from app.models.schemas import Offer, NegotiationState
from app.core.rules import urgency_score
class SellerAgent(GroqAgent):
    def __init__(self): super().__init__("seller negotiation agent")
    def propose(self,state:NegotiationState)->Offer:
        s,b=state.seller,state.buyer
        last=next((o for o in reversed(state.offers) if o.actor=="buyer"),None)
        instruction=(
          f"Return keys price_per_kg, quantity_kg, decision, rationale. "
          f"Seller floor={s.min_price}; normal={s.normal_price}; available={s.quantity_kg}; "
          f"buyer ceiling={b.max_price}; buyer needs={b.quantity_kg}; urgency={urgency_score(s)}/100; "
          f"last buyer offer={last.price_per_kg if last else 'none'}. "
          "Never go below floor. Decision is offer/counter/accept/reject. Rationale under 20 words."
        )
        return Offer(actor="seller",**self.json_call(instruction))
