from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .database import Base, engine
from .routers import admin, auth, orders, products

app = FastAPI(title="Algo Novo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, same_site="lax", https_only=False)

Base.metadata.create_all(engine)

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
UPLOAD_DIR = BACKEND_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"ok": True}


# ---- Serve frontend (same origin so cookies work) ----
app.mount("/css", StaticFiles(directory=str(PROJECT_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(PROJECT_DIR / "js")), name="js")
app.mount("/html", StaticFiles(directory=str(PROJECT_DIR / "html"), html=True), name="html")


@app.get("/")
def root():
    return RedirectResponse(url="/html/Algo Novo.dc.html")
