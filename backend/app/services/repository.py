from datetime import datetime,timezone
from app.db.supabase import get_supabase
from app.models.schemas import NegotiationState,SellerLot,BuyerRequirement,Offer
class NegotiationRepository:
    def __init__(self): self.db=get_supabase()
    def save(self,s:NegotiationState):
        self.db.table("negotiations").upsert({
          "id":s.id,"status":s.status,"round":s.round,"max_rounds":s.max_rounds,
          "seller_data":s.seller.model_dump(),"buyer_data":s.buyer.model_dump(),
          "agreed_price":s.agreed_price,"agreed_quantity":s.agreed_quantity,
          "offers":[o.model_dump() for o in s.offers],"events":s.events,
          "updated_at":datetime.now(timezone.utc).isoformat()}).execute()
        return s
    def _state(self,r):
        return NegotiationState(id=r["id"],status=r["status"],round=r["round"],max_rounds=r.get("max_rounds",6),
          seller=SellerLot(**r["seller_data"]),buyer=BuyerRequirement(**r["buyer_data"]),
          offers=[Offer(**o) for o in (r.get("offers") or [])],agreed_price=r.get("agreed_price"),
          agreed_quantity=r.get("agreed_quantity"),events=r.get("events") or [])
    def get(self,id):
        x=self.db.table("negotiations").select("*").eq("id",id).limit(1).execute()
        return self._state(x.data[0]) if x.data else None
    def completed(self):
        x=self.db.table("negotiations").select("*").eq("status","COMPLETED").execute()
        return [self._state(r) for r in (x.data or [])]
    def create_transaction(self,s):
        self.db.table("transactions").upsert({"negotiation_id":s.id,"product":s.seller.product,
          "quantity_kg":s.agreed_quantity,"price_per_kg":s.agreed_price,
          "total_value":float(s.agreed_quantity or 0)*float(s.agreed_price or 0),
          "seller_business":s.seller.business,"buyer_business":s.buyer.business,"status":"COMPLETED"},
          on_conflict="negotiation_id").execute()
