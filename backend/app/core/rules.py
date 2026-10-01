from app.models.schemas import SellerLot, BuyerRequirement, Offer
class RuleViolation(ValueError): pass
def validate_offer(o:Offer,s:SellerLot,b:BuyerRequirement):
    if o.quantity_kg<=0 or o.quantity_kg>s.quantity_kg: raise RuleViolation("Invalid inventory quantity.")
    if o.quantity_kg>b.quantity_kg: raise RuleViolation("Quantity exceeds buyer requirement.")
    if o.actor=="seller" and o.price_per_kg<s.min_price: raise RuleViolation("Seller floor violation.")
    if o.actor=="buyer" and o.price_per_kg>b.max_price: raise RuleViolation("Buyer ceiling violation.")
    if s.remaining_hours<=0: raise RuleViolation("Commercial window expired.")
    return o
def urgency_score(s:SellerLot)->int:
    time=max(0,min(100,100-(s.remaining_hours/72*100)))
    inv=max(0,min(100,s.quantity_kg/5)); storage=20 if s.storage.lower() in {"chilled","cold"} else 55
    return round(.65*time+.20*inv+.15*storage)
