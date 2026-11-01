from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    category_type: Literal["income", "expense"]

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category_type: Literal["income", "expense"]

    model_config = {
        "from_attributes": True
    }



