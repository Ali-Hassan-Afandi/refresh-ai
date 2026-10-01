from uuid import uuid4
from app.models.schemas import NegotiationState,StartNegotiationRequest,Offer
from app.agents.seller import SellerAgent
from app.agents.buyer import BuyerAgent
from app.agents.logistics import check_logistics
from app.agents.risk import risk_check
from app.core.rules import validate_offer
from app.core.config import settings
from app.services.repository import NegotiationRepository
repo=NegotiationRepository()
def fallback(actor,state):
    s,b=state.seller,state.buyer;q=min(s.quantity_kg,b.quantity_kg)
    if actor=="seller":
        arr=[750,680,610,600,590,580];p=max(s.min_price,min(s.normal_price,arr[min(state.round-1,5)]))
        return Offer(actor="seller",price_per_kg=p,quantity_kg=q,decision="offer",rationale="Price adjusted within seller policy.")
    last=next((o for o in reversed(state.offers) if o.actor=="seller"),None)
    if last and last.price_per_kg<=b.max_price:
        return Offer(actor="buyer",price_per_kg=last.price_per_kg,quantity_kg=q,decision="accept",rationale="Offer fits budget and quantity.")
    arr=[550,590,600,610,620,620];p=min(b.max_price,arr[min(state.round-1,5)])
    return Offer(actor="buyer",price_per_kg=p,quantity_kg=q,decision="counter",rationale="Counteroffer remains within budget.")
def start(req):
    return repo.save(NegotiationState(id=str(uuid4())[:8],seller=req.seller,buyer=req.buyer,events=[{"type":"state","value":"NEGOTIATING"}]))
def step(s):
    if s.status!="NEGOTIATING": return s
    s.round+=1
    for actor,Agent in [("seller",SellerAgent),("buyer",BuyerAgent)]:
        try: o=Agent().propose(s);validate_offer(o,s.seller,s.buyer)
        except Exception as e:
            if not settings.demo_fallback: raise
            o=fallback(actor,s);validate_offer(o,s.seller,s.buyer);s.events.append({"type":"fallback","actor":actor,"reason":str(e)[:140]})
        s.offers.append(o);s.events.append({"type":"offer","actor":actor,"price":o.price_per_kg,"decision":o.decision})
        if actor=="buyer" and o.decision=="accept":
            so=next(x for x in reversed(s.offers[:-1]) if x.actor=="seller")
            s.agreed_price=so.price_per_kg;s.agreed_quantity=min(so.quantity_kg,o.quantity_kg);s.status="AGREEMENT_REACHED";break
    if s.round>=s.max_rounds and s.status=="NEGOTIATING": s.status="REJECTED"
    return repo.save(s)
def run_all(s):
    while s.status=="NEGOTIATING": s=step(s)
    if s.status=="AGREEMENT_REACHED":
        s.status="LOGISTICS_CHECK";lg=check_logistics(s.seller,s.buyer);s.events.append({"type":"logistics","data":lg.model_dump()})
        if lg.status=="NOT_FEASIBLE": s.status="REJECTED";return repo.save(s)
        s.status="RISK_CHECK";risk=risk_check(s);s.events.append({"type":"risk","data":risk});s.status="AWAITING_APPROVAL" if risk["passed"] else "REJECTED"
    return repo.save(s)
def approve(s):
    if s.status!="AWAITING_APPROVAL": raise ValueError(f"Cannot approve from {s.status}")
    s.status="COMPLETED";s.events.append({"type":"approval","value":"APPROVED"});repo.save(s);repo.create_transaction(s);return s
