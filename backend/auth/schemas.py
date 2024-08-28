from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    is_active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"