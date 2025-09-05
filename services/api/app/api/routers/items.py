from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.menu import Item, Category
from app.schemas.menu import ItemDetail, ItemSummary
from app.schemas.errors import ErrorResponse, ErrorCodes

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", response_model=ItemDetail)
def get_item_detail(item_id: int, db: Session = Depends(get_db)):
    """
    Get item details with pairings (related items from same category).
    """
    # Get the item
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error={
                    "code": ErrorCodes.NOT_FOUND,
                    "message": f"Item with id '{item_id}' not found"
                }
            ).dict()["error"]
        )
    
    # Get pairings (other items from the same category, excluding current item)
    pairings = (
        db.query(Item)
        .filter(
            Item.category_id == item.category_id,
            Item.id != item_id
        )
        .limit(6)  # Limit to 6 pairings
        .all()
    )
    
    # Convert pairings to summary format
    pairing_summaries = [
        ItemSummary(
            id=pairing.id,
            name=pairing.name,
            price=pairing.price_cents / 100.0
        )
        for pairing in pairings
    ]
    
    return ItemDetail(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price_cents / 100.0,
        pairings=pairing_summaries
    )


