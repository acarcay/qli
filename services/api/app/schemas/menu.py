from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    branch_id: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: str | None = None


class MenuOut(MenuBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    menu_id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price_cents: int
    category_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price_cents: int | None = None


class ItemOut(ItemBase):
    id: int

    class Config:
        from_attributes = True


# Response schemas for API endpoints
class ItemSummary(BaseModel):
    """Summary item info for menu listings"""
    id: int
    name: str
    price: float  # Converted from price_cents

    class Config:
        from_attributes = True


class CategoryWithItems(BaseModel):
    """Category with first 12 items"""
    id: int
    name: str
    items: list[ItemSummary]

    class Config:
        from_attributes = True


class MenuResponse(BaseModel):
    """Menu response with categories and pagination"""
    categories: list[CategoryWithItems]
    pagination: dict[str, int]  # current_page, total_pages, has_next


class ItemDetail(BaseModel):
    """Detailed item info with pairings"""
    id: int
    name: str
    description: str | None
    price: float
    pairings: list[ItemSummary]  # Related items

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    """Search result item"""
    id: int
    name: str
    price: float
    category_name: str

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Search response with results and pagination"""
    results: list[SearchResult]
    total: int
    page: int
    has_next: bool


class ItemOptionBase(BaseModel):
    name: str
    price_delta_cents: int
    item_id: int


class ItemOptionCreate(ItemOptionBase):
    pass


class ItemOptionUpdate(BaseModel):
    name: str | None = None
    price_delta_cents: int | None = None


class ItemOptionOut(ItemOptionBase):
    id: int

    class Config:
        from_attributes = True



