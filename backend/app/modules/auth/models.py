from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class GoogleLoginInput(SQLModel):
    credential: str | None = None
    token: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    avatar_url: str | None = None
