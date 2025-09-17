from pydantic import BaseModel, ConfigDict, Field


class UserOut(BaseModel):
    first_name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    email: str = Field(..., examples=["john.doe@example.com"])
    phone_number: str = Field(..., examples=["+92-300-0000000"])

    model_config = ConfigDict(from_attributes=True)
