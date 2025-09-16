from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequet(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
