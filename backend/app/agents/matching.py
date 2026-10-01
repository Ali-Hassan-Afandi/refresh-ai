from app.models.schemas import SellerLot,BuyerRequirement
def match_score(s:SellerLot,b:BuyerRequirement):
    product=1 if s.product.lower()==b.product.lower() else 0
    qty=min(1,s.quantity_kg/max(b.quantity_kg,1)); overlap=1 if s.min_price<=b.max_price else 0
    score=round(100*(.5*product+.2*qty+.3*overlap))
    return {"score":score,"compatible":score>=70}
