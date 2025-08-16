from database import Base, engine
from models.db_models import Brand, Product

print("🔄 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
