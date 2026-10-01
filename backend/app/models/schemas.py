from typing import Literal, Optional
from pydantic import BaseModel, Field
class SellerLot(BaseModel):
    business: str="FreshMart Wholesale"; product: str="Strawberries"; quantity_kg: float=50
    normal_price: float=900; min_price: float=550; remaining_hours: float=48
    storage: str="Chilled"; location: str="Multan"
class BuyerRequirement(BaseModel):
    business: str="Royal Restaurant"; product: str="Strawberries"; quantity_kg: float=20
    max_price: float=620; delivery_within_hours: float=5; location: str="Multan"
class Offer(BaseModel):
    actor: Literal["seller","buyer"]; price_per_kg: float; quantity_kg: float
    decision: Literal["offer","counter","accept","reject"]="offer"
    rationale: str=Field(max_length=180)
class NegotiationState(BaseModel):
    id: str; status: str="NEGOTIATING"; round: int=0; max_rounds: int=6
    seller: SellerLot; buyer: BuyerRequirement; offers: list[Offer]=[]
    agreed_price: Optional[float]=None; agreed_quantity: Optional[float]=None
    events: list[dict]=[]
class StartNegotiationRequest(BaseModel):
    seller: SellerLot=SellerLot(); buyer: BuyerRequirement=BuyerRequirement()
class LogisticsResult(BaseModel):
    status: Literal["FEASIBLE","CONDITIONALLY_FEASIBLE","NOT_FEASIBLE"]
    distance_km: float; eta_minutes: int; estimated_cost: float; reason: str
