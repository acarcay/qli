from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, text
from app.db.session import get_db
from app.models.menu import Item, Category
from app.schemas.menu import SearchResponse, SearchResult
from app.schemas.errors import ErrorResponse, ErrorCodes

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search_items(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Search items by name and description using ILIKE or FTS.
    """
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error={
                    "code": ErrorCodes.VALIDATION_ERROR,
                    "message": "Search query cannot be empty"
                }
            ).dict()["error"]
        )
    
    # Use FTS (Full Text Search) if available, fallback to ILIKE
    try:
        # Try FTS first
        search_query = text("""
            SELECT i.id, i.name, i.price_cents, c.name as category_name
            FROM item i
            JOIN category c ON i.category_id = c.id
            WHERE to_tsvector('simple', coalesce(i.name,'') || ' ' || coalesce(i.description,'')) 
                  @@ plainto_tsquery('simple', :query)
            ORDER BY ts_rank(to_tsvector('simple', coalesce(i.name,'') || ' ' || coalesce(i.description,'')), 
                           plainto_tsquery('simple', :query)) DESC
            LIMIT :limit OFFSET :offset
        """)
        
        # Count query for FTS
        count_query = text("""
            SELECT COUNT(*)
            FROM item i
            WHERE to_tsvector('simple', coalesce(i.name,'') || ' ' || coalesce(i.description,'')) 
                  @@ plainto_tsquery('simple', :query)
        """)
        
        offset = (page - 1) * limit
        
        # Execute FTS search
        results = db.execute(
            search_query, 
            {"query": q, "limit": limit, "offset": offset}
        ).fetchall()
        
        total_count = db.execute(count_query, {"query": q}).scalar()
        
    except Exception:
        # Fallback to ILIKE search
        search_term = f"%{q}%"
        offset = (page - 1) * limit
        
        # Build ILIKE query
        query = (
            db.query(Item.id, Item.name, Item.price_cents, Category.name.label("category_name"))
            .join(Category, Item.category_id == Category.id)
            .filter(
                or_(
                    Item.name.ilike(search_term),
                    Item.description.ilike(search_term)
                )
            )
            .order_by(Item.name)
        )
        
        # Get total count
        total_count = (
            db.query(Item)
            .filter(
                or_(
                    Item.name.ilike(search_term),
                    Item.description.ilike(search_term)
                )
            )
            .count()
        )
        
        # Get paginated results
        results = query.offset(offset).limit(limit).all()
    
    # Convert results to response format
    search_results = [
        SearchResult(
            id=result.id,
            name=result.name,
            price=result.price_cents / 100.0,
            category_name=result.category_name
        )
        for result in results
    ]
    
    has_next = (offset + limit) < total_count
    
    return SearchResponse(
        results=search_results,
        total=total_count,
        page=page,
        has_next=has_next
    )
