import random
import sys
import os

# Add the project root to the Python path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

        # Create Categories for Grinding Wheel Industry
        categories_data = [
            Category(name="木工锯片行业砂轮", sort_order=1),
            Category(name="铣刀钻头行业砂轮", sort_order=2),
            Category(name="周边磨砂轮", sort_order=3),
            Category(name="研磨高速钢锯片专用CBN砂轮", sort_order=4),
            Category(name="外圆磨平面磨大直径平行砂轮、磨盘系列", sort_order=5),
            Category(name="锯片基体专用CBN砂轮", sort_order=6),
            Category(name="研磨热喷涂合金粉CBN砂轮", sort_order=7),
            Category(name="TCT开料刀专用砂轮", sort_order=8),
            Category(name="切铁锯片专用砂轮", sort_order=9),
            Category(name="合金带锯条专用砂轮", sort_order=10),
            Category(name="刀具行业砂轮", sort_order=11),
            Category(name="研磨丝锥专用CBN砂轮", sort_order=12),
        ]
        db.add_all(categories_data)
        db.commit()
        print(f"{len(categories_data)} categories created.")

        # Create Banners
        banners_data = [
            Banner(image_url="uploads/sample_banner1.jpg", link_url="", sort_order=1, is_active=True),
            Banner(image_url="uploads/sample_banner2.jpg", link_url="", sort_order=2, is_active=True),
        ]
        db.add_all(banners_data)
        db.commit()
        print(f"{len(banners_data)} banners created.")

        # --- Create Products with Randomized Data ---
        print("Generating products with new categories...")
        products_to_create = []
        
        # Pre-defined descriptions for variety
        descriptions = [
            "高品质金刚石砂轮，专为精密磨削设计。",
            "CBN立方氮化硼砂轮，适用于高速钢和硬质合金。",
            "树脂结合剂砂轮，具有优异的自锐性和切削效率。",
            "陶瓷结合剂砂轮，耐用性强，形状保持性好。",
            "金属结合剂砂轮，适合重负荷磨削和成型磨削。",
            "电镀砂轮，用于复杂型面的精密加工。"
        ]

        # Specific products for certain categories
        specific_products = {
            "木工锯片行业砂轮": [
                "汉德，潞汰设备配套砂轮", "夏田，拓思设备配套砂轮", "威猛，百博设备配套砂轮",
                "木工刀具生产配套砂轮", "胶木基体砂轮", "星野设备配套砂轮"
            ],
            "铣刀钻头行业砂轮": [
                "强力开槽砂轮", "树脂开槽砂轮", "6V5砂轮", "12V9砂轮",
                "11V9砂轮", "1V1砂轮", "无心磨砂轮", "钨钢切割片"
            ]
        }

        for category in categories_data:
            if category.name in specific_products:
                for product_name in specific_products[category.name]:
                    products_to_create.append(Product(
                        name=product_name,
                        description=random.choice(descriptions),
                        price=round(random.uniform(100, 1000), 2),
                        stock_quantity=100,
                        sales=0,
                        category=category.name
                    ))
            else:
                # For other categories, create one product with the same name
                products_to_create.append(Product(
                    name=category.name, # Product name is same as category
                    description=random.choice(descriptions),
                    price=round(random.uniform(100, 1000), 2),
                    stock_quantity=100,
                    sales=0,
                    category=category.name
                ))
        
        db.add_all(products_to_create)
        db.commit()
        print(f"{len(products_to_create)} products created.")

        # Assign the newly created products to products_data for stock movement creation
        products_data = products_to_create

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
