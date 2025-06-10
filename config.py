# core/models/config.py

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve()

class AuthJWT(BaseModel):
    private_key_path: Path
    public_key_path: Path
    algorithm: str = "RS256"


class Setting(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    
    
    api_v1_prefix: str = "/api/v1"

    db_url:str
    db_echo: bool = False

    private_key_path: Path
    public_key_path: Path
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60 * 30
    refresh_token_expire_days: int = 86400 * 15

    minio_root_user: str
    minio_root_password: str
    minio_port: int
    minio_console_port: int

    # S3
    s3_access_key: str
    s3_secret_key: str
    s3_endpoint_url: str
    s3_bucket_name: str
    
    
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env",extra="ignore",env_file_encoding='utf-8')
    @property
    def auth_jwt(self) -> AuthJWT:
        return AuthJWT(
            private_key_path=self.private_key_path,
            public_key_path=self.public_key_path,
            algorithm=self.algorithm
        )




settings = Setting()
# print(settings.db_url)
