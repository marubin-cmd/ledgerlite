from pydantic import BaseModel, ConfigDict, Field, EmailStr


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    address: str | None = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr | None
    phone: str | None
    address: str | None

    model_config = ConfigDict(from_attributes=True)