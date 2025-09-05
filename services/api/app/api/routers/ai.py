from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/upsell")
def suggest_upsell():
    return {"suggestions": []}


