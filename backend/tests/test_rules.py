import pytest
from app.models.schemas import SellerLot,BuyerRequirement,Offer
from app.core.rules import validate_offer,RuleViolation
def test_floor():
    with pytest.raises(RuleViolation): validate_offer(Offer(actor="seller",price_per_kg=500,quantity_kg=20,rationale="x"),SellerLot(),BuyerRequirement())
def test_ceiling():
    with pytest.raises(RuleViolation): validate_offer(Offer(actor="buyer",price_per_kg=700,quantity_kg=20,rationale="x"),SellerLot(),BuyerRequirement())
