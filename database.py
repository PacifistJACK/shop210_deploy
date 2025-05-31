from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch connection string and secret key
db_connection_link = os.getenv("DB_CONNECTION_LINK").strip('"')
secret_key = os.getenv("SECRET_KEY")

# Path to CA certificate (ensure this path is correct)
ca_cert_path = r"D:\Shop\Shop210\ca.pem"

# Create SQLAlchemy engine with SSL using pymysql
engine = create_engine(
    db_connection_link,
    connect_args={"ssl": {"ca": ca_cert_path}}
)

# Fetch items for a specific category
def fetch_items_by_category(category_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name, image_url, price FROM items WHERE category_id = :id"),
            {"id": category_id}
        )
        return result.fetchall()

# Fetch all categories
def fetch_categories():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, image_url FROM categories"))
        return result.fetchall()
    
def fetch_items_by_category(category_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, image_url, price FROM items WHERE category_id = :id"),
            {"id": category_id}
        )
        return result.fetchall()
    
def get_item_by_id(item_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, image_url, price FROM items WHERE id = :id"),
            {"id": item_id}
        )
        return result.fetchone()


