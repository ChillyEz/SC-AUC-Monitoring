from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SC-AUC-Monitoring"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENV: Literal["development", "staging", "production"] = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Stalcraft API
    USE_DEMO_API: bool = True
    STALCRAFT_DEMO_HOST: str = "dapi.stalcraft.net"
    STALCRAFT_PROD_HOST: str = "eapi.stalcraft.net"
    STALCRAFT_API_TOKEN: str = ""  # Только для prod
    
    # Regions
    SUPPORTED_REGIONS: list[str] = ["EU", "RU", "NA", "SEA"]
    
    # Items Database
    ITEMS_DB_SOURCE: Literal["github", "local"] = "github"
    GITHUB_DB_REPO: str = "EXBO-Studio/stalcraft-database"
    GITHUB_DB_BRANCH: str = "main"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    @property
    def api_base_url(self) -> str:
        host = self.STALCRAFT_DEMO_HOST if self.USE_DEMO_API else self.STALCRAFT_PROD_HOST
        return f"https://{host}"
    
    @property
    def github_db_base_url(self) -> str:
        return f"https://raw.githubusercontent.com/{self.GITHUB_DB_REPO}/{self.GITHUB_DB_BRANCH}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
