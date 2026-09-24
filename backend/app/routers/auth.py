from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..auth import (
    COOKIE_NAME,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from ..captcha import new_captcha, verify_captcha
from ..config import settings
from ..database import get_db
from ..models import User
from ..oauth import oauth, AUTHLIB_AVAILABLE
from ..schemas import (
    AdminLoginIn,
    AuthOut,
    CaptchaOut,
    LoginIn,
    OAuthAvailability,
    RegisterIn,
    UserOut,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session(response: Response, user_id: int) -> None:
    token = create_access_token(user_id)
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=False,  # set True behind HTTPS
        path="/",
    )


@router.get("/captcha", response_model=CaptchaOut)
def get_captcha():
    token, question = new_captcha()
    return CaptchaOut(token=token, question=question)


@router.get("/oauth-availability", response_model=OAuthAvailability)
def oauth_availability():
    return OAuthAvailability(
        google=settings.oauth_enabled("google"),
        facebook=settings.oauth_enabled("facebook"),
    )


@router.post("/register", response_model=AuthOut)
def register(payload: RegisterIn, response: Response, db: Session = Depends(get_db)):
    if not verify_captcha(payload.captcha_token, payload.captcha_answer):
        raise HTTPException(status_code=400, detail="Captcha inválido")
    if db.query(User).filter(User.email == payload.email).one_or_none():
        raise HTTPException(status_code=400, detail="Email já registado")
    user = User(
        email=payload.email,
        name=payload.name or payload.email.split("@")[0],
        password_hash=hash_password(payload.password),
        role="client",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _set_session(response, user.id)
    return AuthOut(user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthOut)
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    if not verify_captcha(payload.captcha_token, payload.captcha_answer):
        raise HTTPException(status_code=400, detail="Captcha inválido")
    user = db.query(User).filter(User.email == payload.email).one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if user.role == "admin":
        raise HTTPException(status_code=403, detail="Use o login de admin")
    _set_session(response, user.id)
    return AuthOut(user=UserOut.model_validate(user))


@router.post("/admin/login", response_model=AuthOut)
def admin_login(payload: AdminLoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).one_or_none()
    if not user or user.role != "admin" or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    _set_session(response, user.id)
    return AuthOut(user=UserOut.model_validate(user))


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut.model_validate(user)


# ---- OAuth (Google, Facebook) ----
def _redirect_to_frontend(response: RedirectResponse) -> RedirectResponse:
    return response


@router.get("/oauth/{provider}")
async def oauth_start(provider: str, request: Request):
    if not AUTHLIB_AVAILABLE:
        raise HTTPException(status_code=501, detail="OAuth desativado (instale authlib)")
    if not settings.oauth_enabled(provider):
        raise HTTPException(status_code=404, detail="Provider não configurado")
    client = oauth.create_client(provider)
    redirect_uri = f"{settings.oauth_callback_base}/api/auth/oauth/{provider}/callback"
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/oauth/{provider}/callback")
async def oauth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    if not AUTHLIB_AVAILABLE:
        raise HTTPException(status_code=501, detail="OAuth desativado (instale authlib)")
    if not settings.oauth_enabled(provider):
        raise HTTPException(status_code=404, detail="Provider não configurado")
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    email = ""
    name = ""
    sub = ""
    if provider == "google":
        info = token.get("userinfo") or await client.parse_id_token(request, token)
        email = info.get("email", "")
        name = info.get("name", "")
        sub = info.get("sub", "")
    elif provider == "facebook":
        resp = await client.get("me?fields=id,name,email", token=token)
        info = resp.json()
        email = info.get("email", "")
        name = info.get("name", "")
        sub = info.get("id", "")
    if not email:
        raise HTTPException(status_code=400, detail="Email não fornecido pelo provider")

    user = db.query(User).filter(User.email == email).one_or_none()
    if not user:
        user = User(email=email, name=name, role="client", oauth_provider=provider, oauth_sub=sub)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not user.oauth_provider:
            user.oauth_provider = provider
            user.oauth_sub = sub
            db.commit()

    params = urlencode({"oauth": "ok"})
    redirect = RedirectResponse(url=f"{settings.frontend_url}?{params}")
    _set_session(redirect, user.id)
    return redirect
