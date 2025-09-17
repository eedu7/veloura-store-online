from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class LoginRequest(BaseModel):
    email: str = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., examples=["Password@123"])


class RegisterRequet(LoginRequest):
    first_name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    phone_number: PhoneNumber = Field(..., examples=["+92-300-0000000"])


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
