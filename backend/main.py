from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import engine, create_db_and_tables, get_session
from models import Product, Order
from typing import List

app = FastAPI(title="Mercyanna Store API")

# Allow Frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Seed dummy data if empty (Optional for testing)
    with Session(engine) as session:
        if not session.exec(select(Product)).first():
            products = [
                Product(name="Silk Scrunchie Set", description="Soft pastel scrunchies.", price=15.00, category="Accessories", image_url="https://images.unsplash.com/photo-1606103920295-9a091573f160?auto=format&fit=crop&q=80&w=800"),
                Product(name="Rose Gold Necklace", description="Minimalist chain.", price=45.00, category="Jewelry", image_url="https://images.unsplash.com/photo-1599643478518-17488fbbcd75?auto=format&fit=crop&q=80&w=800"),
                Product(name="Cozy Oversized Hoodie", description="Pink fluffy hoodie.", price=60.00, category="Clothes", image_url="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&q=80&w=800"),
                Product(name="Smart Watch Band", description="Pink silicone band.", price=25.00, category="Gadgets", image_url="https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&q=80&w=800"),
            ]
            for p in products:
                session.add(p)
            session.commit()

@app.get("/api/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@app.get("/api/products/{id}", response_model=Product)
def get_product(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/orders")
def create_order(order: Order, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order