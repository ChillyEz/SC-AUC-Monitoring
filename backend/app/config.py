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
    API_SOURCE: Literal["demo", "production", "wiki"] = "wiki"
    USE_DEMO_API: bool = True  # Deprecated: use API_SOURCE instead
    STALCRAFT_DEMO_HOST: str = "dapi.stalcraft.net"
    STALCRAFT_PROD_HOST: str = "eapi.stalcraft.net"
    # Demo API Token (App Access Token - public)
    STALCRAFT_DEMO_TOKEN: str = (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwibmJmIjoxNjczNzk3ODM4LCJleHAiOjQ4MjczOTc4MzgsImlhdCI6MTY3Mzc5NzgzOCwianRpIjoiYXhwbzAzenJwZWxkMHY5dDgzdzc1N2x6ajl1MmdyeHVodXVlb2xsZ3M2dml1YjVva3NwZTJ3eGFrdjJ1eWZxaDU5ZDE2ZTNlN2FqdW16Z3gifQ.ZNSsvwAX72xT5BzLqqYABuH2FGbOlfiXMK5aYO1H5llG51ZjcPvOYBDRR4HUoPZVLFY8jyFUsEXNM7SYz8qL9ePmLjJl6pib8FEtqVPmf9ldXvKkbaaaSp4KkJzsIEMY_Z5PejB2Vr-q-cL13KPgnLGUaSW-2X_sHPN7VZJNMjRgjw4mPiRZTe4CEpQq0BEcPrG6OLtU5qlZ6mLDJBjN2xtK0DI6xgmYriw_5qW1mj1nqF_ewtUiQ1KTVhDgXnaNUdkGsggAGqyicTei0td6DTKtnl3noD5VkipWn_CwSqb2Mhm16I9BPfX_d5ARzWrnrwPRUf6PA_7LipNU6KkkW0mhZfmwEPTm_sXPus0mHPENoVZArdFT3L5sOYBcpqwvVIEtxRUTdcsKp-y-gSzao5muoyPVoCc2LEeHEWx0cIi9spsZ46SPRQpN4baVFp7y5rp5pjRsBKHQYUJ0lTmh1_vyfzOzbtNN2v6W_5w9JTLrN1U6fhmifvKHppFSEqD6DameL1TC59kpIdufRkEU9HE4O-ErEf1GuJFRx-Dew6XDvb_ExhvEqcw31yNvKzpVqLYJfLazqn6tUbVuAiPwpy6rP9tYO2taT1vj5TGn_vxwDu9zoLWe796tFMPS-kmbCglxB5C9L4EbpfWNbWxYjUkTvjT2Ml9OnrB0UbYo1jI"
    )
    # Production API Token (to be provided by user)
    STALCRAFT_PROD_TOKEN: str = ""
    # Unofficial Wiki API (for development/testing only)
    # Note: This is a public API key shared for development purposes
    STALCRAFT_WIKI_HOST: str = "stalcraft.wiki"
    STALCRAFT_WIKI_API_KEY: str = "cb2b4565-a129-4e9c-bbd1-88427f79468d"

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
        if self.API_SOURCE == "wiki":
            return f"https://{self.STALCRAFT_WIKI_HOST}"
        elif self.API_SOURCE == "demo":
            return f"https://{self.STALCRAFT_DEMO_HOST}"
        else:  # production
            return f"https://{self.STALCRAFT_PROD_HOST}"

    @property
    def api_token(self) -> str:
        """Automatically select the appropriate API token"""
        if self.API_SOURCE == "wiki":
            return ""  # Wiki API uses X-Internal-Key header instead
        elif self.API_SOURCE == "demo":
            return self.STALCRAFT_DEMO_TOKEN
        else:  # production
            return self.STALCRAFT_PROD_TOKEN

    @property
    def github_db_base_url(self) -> str:
        return f"https://raw.githubusercontent.com/{self.GITHUB_DB_REPO}/{self.GITHUB_DB_BRANCH}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
