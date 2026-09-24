from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Product
from ..schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    rows = db.query(Product).filter(Product.active == True).order_by(Product.id).all()  # noqa: E712
    return [ProductOut.model_validate(p) for p in rows]
