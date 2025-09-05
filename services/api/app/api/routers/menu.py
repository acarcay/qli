from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.db.session import get_db
from app.models.restaurant import Restaurant
from app.models.menu import Menu, Category, Item
from app.schemas.menu import MenuResponse, CategoryWithItems, ItemSummary
from app.schemas.errors import ErrorResponse, ErrorCodes

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/{restaurant_slug}", response_model=MenuResponse)
def get_menu_by_restaurant_slug(
    restaurant_slug: str,
    page: int = Query(1, ge=1, description="Page number"),
    db: Session = Depends(get_db)
):
    """
    Get menu by restaurant slug with categories and first 12 items per category.
    Supports pagination with ?p= parameter.
    """
    # Find restaurant by slug
    restaurant = db.query(Restaurant).filter(Restaurant.slug == restaurant_slug).first()
    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error={
                    "code": ErrorCodes.NOT_FOUND,
                    "message": f"Restaurant with slug '{restaurant_slug}' not found"
                }
            ).dict()["error"]
        )
    
    # Get the first branch's menu (assuming one menu per branch for now)
    branch = restaurant.branches[0] if restaurant.branches else None
    if not branch:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error={
                    "code": ErrorCodes.NOT_FOUND,
                    "message": f"No menu found for restaurant '{restaurant_slug}'"
                }
            ).dict()["error"]
        )
    
    menu = branch.menus[0] if branch.menus else None
    if not menu:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error={
                    "code": ErrorCodes.NOT_FOUND,
                    "message": f"No menu found for restaurant '{restaurant_slug}'"
                }
            ).dict()["error"]
        )
    
    # Get categories with items (first 12 per category)
    categories = db.query(Category).filter(Category.menu_id == menu.id).all()
    
    categories_with_items = []
    for category in categories:
        # Get first 12 items for this category
        items = (
            db.query(Item)
            .filter(Item.category_id == category.id)
            .limit(12)
            .all()
        )
        
        # Convert to summary format
        item_summaries = [
            ItemSummary(
                id=item.id,
                name=item.name,
                price=item.price_cents / 100.0  # Convert cents to currency
            )
            for item in items
        ]
        
        categories_with_items.append(
            CategoryWithItems(
                id=category.id,
                name=category.name,
                items=item_summaries
            )
        )
    
    # Simple pagination info (for future enhancement)
    pagination = {
        "current_page": page,
        "total_pages": 1,  # For now, all items fit in one page
        "has_next": False
    }
    
    return MenuResponse(
        categories=categories_with_items,
        pagination=pagination
    )


