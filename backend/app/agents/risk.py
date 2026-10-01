from app.models.schemas import NegotiationState
def risk_check(s:NegotiationState):
    issues=[]
    if s.agreed_price is None: issues.append("missing price")
    if s.agreed_quantity is None: issues.append("missing quantity")
    if s.agreed_price and s.agreed_price<s.seller.min_price: issues.append("seller floor")
    if s.agreed_price and s.agreed_price>s.buyer.max_price: issues.append("buyer ceiling")
    return {"passed":not issues,"issues":issues}
