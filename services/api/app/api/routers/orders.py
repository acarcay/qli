from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders():
    return []


