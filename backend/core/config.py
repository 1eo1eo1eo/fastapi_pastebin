from pathlib import Path
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    run: RunConfig = RunConfig()
    db: DataBaseConfig
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings() #type: ignore