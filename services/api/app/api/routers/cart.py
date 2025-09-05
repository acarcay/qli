from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("")
def get_cart():
    return {"items": []}


