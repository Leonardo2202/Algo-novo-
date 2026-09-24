from .database import Base, SessionLocal, engine
from .config import settings
from .models import User, Product
from .auth import hash_password


BASE_PRODUCTS = [
    {"id": "p1", "cat_key": "tshirts",     "price": 24.9, "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=1000&fit=crop"},
    {"id": "p2", "cat_key": "tshirts",     "price": 29.9, "img": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=800&h=1000&fit=crop"},
    {"id": "p3", "cat_key": "hoodies",     "price": 54.9, "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&h=1000&fit=crop"},
    {"id": "p4", "cat_key": "hoodies",     "price": 46.9, "img": "https://images.unsplash.com/photo-1578681994506-b8f463449011?w=800&h=1000&fit=crop"},
    {"id": "p5", "cat_key": "embroidery",  "price": 39.9, "img": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=800&h=1000&fit=crop"},
    {"id": "p6", "cat_key": "accessories", "price": 22.9, "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&h=1000&fit=crop"},
    {"id": "p7", "cat_key": "accessories", "price": 16.9, "img": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=800&h=1000&fit=crop"},
    {"id": "p8", "cat_key": "hoodies",     "price": 62.9, "img": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&h=1000&fit=crop"},
]


def run():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.admin_email).one_or_none()
        if not admin:
            admin = User(
                email=settings.admin_email,
                name="Admin",
                password_hash=hash_password(settings.admin_password),
                role="admin",
            )
            db.add(admin)
            print(f"[seed] admin created: {settings.admin_email}")
        else:
            print(f"[seed] admin exists: {settings.admin_email}")

        client_email = "cliente@algonovo.pt"
        client = db.query(User).filter(User.email == client_email).one_or_none()
        if not client:
            client = User(
                email=client_email,
                name="Cliente",
                password_hash=hash_password("1234567"),
                role="client",
            )
            db.add(client)
            print(f"[seed] cliente criado: {client_email} (senha: 1234567)")
        else:
            print(f"[seed] cliente exists: {client_email}")

        for p in BASE_PRODUCTS:
            existing = db.get(Product, p["id"])
            if existing:
                continue
            db.add(Product(**p, active=True))
        db.commit()
        print(f"[seed] products ensured ({len(BASE_PRODUCTS)})")
    finally:
        db.close()


if __name__ == "__main__":
    run()
