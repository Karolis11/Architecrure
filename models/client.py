from pydantic import BaseModel, EmailStr, Field

class Client(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    age: int

class ClientIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    phone: str = Field(min_length=6, max_length=20)
    age: int = Field(ge=18, le=120)
