from fastapi import APIRouter,HTTPException
from app.models.schemas import StartNegotiationRequest
from app.agents.matching import match_score
from app.services.negotiation import start,step,run_all,approve,repo
from app.db.supabase import get_supabase
router=APIRouter()
@router.get("/database-test")
def dbtest():
    r=get_supabase().table("negotiations").select("id").limit(1).execute()
    return {"status":"connected","database":"supabase","records":len(r.data or [])}
@router.get("/demo")
def demo():
    r=StartNegotiationRequest();return {"seller":r.seller,"buyer":r.buyer,"match":match_score(r.seller,r.buyer)}
@router.post("/negotiations/start")
def startn(r:StartNegotiationRequest): return start(r)
@router.get("/negotiations/{id}")
def getn(id:str):
    s=repo.get(id)
    if not s: raise HTTPException(404,"Negotiation not found")
    return s
@router.post("/negotiations/{id}/run")
def runn(id:str):
    s=repo.get(id)
    if not s: raise HTTPException(404,"Negotiation not found")
    return run_all(s)
@router.post("/transactions/{id}/approve")
def appr(id:str):
    s=repo.get(id)
    if not s: raise HTTPException(404,"Negotiation not found")
    try:return approve(s)
    except ValueError as e:raise HTTPException(409,str(e))
@router.get("/analytics/summary")
def analytics():
    c=repo.completed()
    return {"food_rescued_kg":sum(x.agreed_quantity or 0 for x in c),
      "seller_revenue_recovered":sum((x.agreed_quantity or 0)*(x.agreed_price or 0) for x in c),
      "buyer_savings":sum((x.agreed_quantity or 0)*(x.seller.normal_price-(x.agreed_price or 0)) for x in c),
      "completed_deals":len(c)}
