import json
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Order, OrderItem, Product, User
from ..schemas import OrderOut

router = APIRouter(prefix="/api/orders", tags=["orders"])

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("", response_model=OrderOut)
async def create_order(
    lang: str = Form("pt"),
    project_nome: str = Form(""),
    project_email: str = Form(""),
    project_desc: str = Form(""),
    items_json: str = Form("[]"),          # [{"product_id":"p1","qty":2}, ...]
    custom_sizes_json: str = Form("{}"),   # {"S":1,"M":2}
    art: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        items = json.loads(items_json or "[]")
        custom_sizes = json.loads(custom_sizes_json or "{}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    art_path = ""
    art_name = ""
    if art is not None and art.filename:
        ext = os.path.splitext(art.filename)[1].lower() or ".bin"
        stored = f"{uuid.uuid4().hex}{ext}"
        dest = UPLOAD_DIR / stored
        with dest.open("wb") as f:
            f.write(await art.read())
        art_path = f"/uploads/{stored}"
        art_name = art.filename

    order = Order(
        user_id=user.id,
        status="recebido",
        lang=lang,
        project_nome=project_nome,
        project_email=project_email,
        project_desc=project_desc,
        custom_sizes=custom_sizes or {},
        art_path=art_path,
        art_name=art_name,
    )
    db.add(order)
    db.flush()

    total = 0.0
    for it in items:
        pid = str(it.get("product_id", ""))
        qty = int(it.get("qty", 0))
        if qty <= 0 or not pid:
            continue
        prod = db.get(Product, pid)
        if not prod:
            continue
        unit = float(prod.price)
        db.add(OrderItem(
            order_id=order.id,
            product_id=pid,
            product_name=it.get("product_name", pid),
            qty=qty,
            unit_price=unit,
        ))
        total += unit * qty
    order.total = total
    db.commit()
    db.refresh(order)
    return OrderOut.model_validate(order)


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Order).order_by(Order.created_at.desc())
    if user.role != "admin":
        q = q.filter(Order.user_id == user.id)
    return [OrderOut.model_validate(o) for o in q.all()]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    o = db.get(Order, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if user.role != "admin" and o.user_id != user.id:
        raise HTTPException(status_code=403, detail="Sem acesso")
    return OrderOut.model_validate(o)
