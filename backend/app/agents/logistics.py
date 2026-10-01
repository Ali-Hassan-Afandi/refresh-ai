from app.models.schemas import SellerLot,BuyerRequirement,LogisticsResult
def check_logistics(s:SellerLot,b:BuyerRequirement):
    distance,eta,cost=12.4,34,850.0
    ok=eta/60<b.delivery_within_hours and eta/60+1<s.remaining_hours
    return LogisticsResult(status="FEASIBLE" if ok else "NOT_FEASIBLE",distance_km=distance,eta_minutes=eta,estimated_cost=cost,reason="Timing feasible." if ok else "Timing infeasible.")
