from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = "dev-secret-change-me"
    database_url: str = "sqlite:///./algonovo.db"
    access_token_minutes: int = 1440
    cors_origins: str = "http://localhost:5500,http://127.0.0.1:5500"

    admin_email: str = "admin@algonovo.pt"
    admin_password: str = "1234567"

    frontend_url: str = "http://127.0.0.1:5500/html/Algo Novo.dc.html"
    oauth_callback_base: str = "http://127.0.0.1:8000"

    google_client_id: str = ""
    google_client_secret: str = ""

    facebook_client_id: str = ""
    facebook_client_secret: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def oauth_enabled(self, provider: str) -> bool:
        if provider == "google":
            return bool(self.google_client_id and self.google_client_secret)
        if provider == "facebook":
            return bool(self.facebook_client_id and self.facebook_client_secret)
        return False


settings = Settings()
