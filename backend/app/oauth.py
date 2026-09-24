from .config import settings

try:
    from authlib.integrations.starlette_client import OAuth
    _AUTHLIB_OK = True
except Exception:  # authlib not installed
    _AUTHLIB_OK = False


class _NoOAuth:
    def create_client(self, name):
        return None

    def __getattr__(self, name):
        return None


if _AUTHLIB_OK:
    oauth = OAuth()
    if settings.google_client_id and settings.google_client_secret:
        oauth.register(
            name="google",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )
    if settings.facebook_client_id and settings.facebook_client_secret:
        oauth.register(
            name="facebook",
            client_id=settings.facebook_client_id,
            client_secret=settings.facebook_client_secret,
            access_token_url="https://graph.facebook.com/v18.0/oauth/access_token",
            authorize_url="https://www.facebook.com/v18.0/dialog/oauth",
            api_base_url="https://graph.facebook.com/v18.0/",
            client_kwargs={"scope": "email public_profile"},
        )
else:
    oauth = _NoOAuth()


AUTHLIB_AVAILABLE = _AUTHLIB_OK
