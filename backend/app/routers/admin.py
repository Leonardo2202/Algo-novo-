from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import Order, Product, User
from ..schemas import OrderOut, OrderStatusIn, ProductOut, ProductUpdateIn

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/products", response_model=list[ProductOut])
def list_all_products(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rows = db.query(Product).order_by(Product.id).all()
    return [ProductOut.model_validate(p) for p in rows]


@router.patch("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str,
    payload: ProductUpdateIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return ProductOut.model_validate(p)


@router.patch("/orders/{order_id}", response_model=OrderOut)
def update_order_status(
    order_id: int,
    payload: OrderStatusIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    o.status = payload.status
    db.commit()
    db.refresh(o)
    return OrderOut.model_validate(o)
