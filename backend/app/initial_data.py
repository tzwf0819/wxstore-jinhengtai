from app.core.db import engine, Base, SessionLocal
from app.models.banner import Banner
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.stock import StockMovement, StockMovementType # Import stock models

def init_db():
    print("--- Database Initialization ---")
    print(f"Connecting to database: {engine.url}")

    # Drop all tables first to ensure a clean state
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")

    # Create all tables
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # Create a new session
    db = SessionLocal()

    try:
        print("Populating database with initial data...")

        # Create Categories
        categories_data = [
            Category(name="手机数码", sort_order=1),
            Category(name="家用电器", sort_order=2),
            Category(name="服饰鞋靴", sort_order=3),
            Category(name="美妆护肤", sort_order=4),
        ]
        db.add_all(categories_data)
        db.commit()
        print(f"{len(categories_data)} categories created.")

        # Create Banners
        banners_data = [
            Banner(image_url="https://via.placeholder.com/750x300.png/0000FF/FFFFFF?Text=Banner1", link_url="/pages/product/detail/detail?id=1", sort_order=1),
            Banner(image_url="https://via.placeholder.com/750x300.png/FF0000/FFFFFF?Text=Banner2", link_url="/pages/product/detail/detail?id=2", sort_order=2),
        ]
        db.add_all(banners_data)
        db.commit()
        print(f"{len(banners_data)} banners created.")

        # Create Products with initial stock and category
        products_data = [
            Product(name="智能手机Pro", description="最新款旗舰智能手机", price=4999.00, stock_quantity=100, sales=50, category="手机数码"),
            Product(name="高清智能电视", description="55英寸4K高清电视", price=2999.00, stock_quantity=50, sales=20, category="家用电器"),
            Product(name="潮流运动鞋", description="舒适透气，适合运动和日常穿着", price=499.00, stock_quantity=200, sales=100, category="服饰鞋靴"),
            Product(name="保湿面霜", description="深层滋润，长效保湿", price=199.00, stock_quantity=150, sales=80, category="美妆护肤"),
        ]
        db.add_all(products_data)
        db.commit()
        print(f"{len(products_data)} products created with initial stock.")

        # Create initial stock movements for each product
        for product in products_data:
            initial_movement = StockMovement(
                product_id=product.id,
                quantity=product.stock_quantity,
                movement_type=StockMovementType.INITIAL.value,
                reference_id="initial_setup"
            )
            db.add(initial_movement)
        db.commit()
        print("Initial stock movements created.")

        print("Initial data populated successfully.")

    finally:
        db.close()
        print("--- Database Initialization Complete ---")

if __name__ == "__main__":
    init_db()
