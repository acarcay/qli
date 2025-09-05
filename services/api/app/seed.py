"""Simple seed script to populate demo data.

Usage:
    python -m app.seed
"""

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models import Restaurant, Branch, Table, Menu, Category, Item


def seed(db: Session) -> None:
    if db.query(Restaurant).count() > 0:
        return

    r = Restaurant(name="Qlick Demo Restaurant", slug="qlick-demo")
    db.add(r)
    db.flush()

    b = Branch(name="Main Branch", restaurant_id=r.id)
    db.add(b)
    db.flush()

    t = Table(code="T1", branch_id=b.id)
    db.add(t)

    m = Menu(title="Main Menu", branch_id=b.id)
    db.add(m)
    db.flush()

    cats = [
        Category(name="Appetizers", menu_id=m.id),
        Category(name="Main Courses", menu_id=m.id),
        Category(name="Beverages", menu_id=m.id),
        Category(name="Desserts", menu_id=m.id),
    ]
    db.add_all(cats)
    db.flush()

    # Appetizers
    appetizers = [
        Item(name="Caesar Salad", description="Fresh romaine lettuce with caesar dressing", price_cents=1299, category_id=cats[0].id),
        Item(name="Buffalo Wings", description="Spicy chicken wings with blue cheese dip", price_cents=1599, category_id=cats[0].id),
        Item(name="Mozzarella Sticks", description="Crispy breaded mozzarella with marinara sauce", price_cents=1199, category_id=cats[0].id),
        Item(name="Chicken Quesadilla", description="Grilled chicken with cheese and peppers", price_cents=1399, category_id=cats[0].id),
    ]
    
    # Main Courses
    mains = [
        Item(name="Grilled Salmon", description="Fresh Atlantic salmon with lemon butter sauce", price_cents=2499, category_id=cats[1].id),
        Item(name="Beef Burger", description="Juicy beef patty with lettuce, tomato, and onion", price_cents=1899, category_id=cats[1].id),
        Item(name="Chicken Parmesan", description="Breaded chicken with marinara and mozzarella", price_cents=2199, category_id=cats[1].id),
        Item(name="Pasta Carbonara", description="Creamy pasta with bacon and parmesan", price_cents=1799, category_id=cats[1].id),
        Item(name="Ribeye Steak", description="12oz ribeye steak cooked to perfection", price_cents=3299, category_id=cats[1].id),
        Item(name="Fish and Chips", description="Beer-battered cod with crispy fries", price_cents=1999, category_id=cats[1].id),
    ]
    
    # Beverages
    beverages = [
        Item(name="Coca Cola", description="Classic cola drink", price_cents=299, category_id=cats[2].id),
        Item(name="Fresh Orange Juice", description="Freshly squeezed orange juice", price_cents=499, category_id=cats[2].id),
        Item(name="Coffee", description="Freshly brewed coffee", price_cents=399, category_id=cats[2].id),
        Item(name="Iced Tea", description="Refreshing iced tea", price_cents=299, category_id=cats[2].id),
    ]
    
    # Desserts
    desserts = [
        Item(name="Chocolate Cake", description="Rich chocolate cake with vanilla ice cream", price_cents=899, category_id=cats[3].id),
        Item(name="Tiramisu", description="Classic Italian dessert", price_cents=799, category_id=cats[3].id),
        Item(name="Apple Pie", description="Warm apple pie with cinnamon", price_cents=699, category_id=cats[3].id),
    ]
    
    all_items = appetizers + mains + beverages + desserts
    db.add_all(all_items)
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)


if __name__ == "__main__":
    main()



