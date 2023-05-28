from pydantic import BaseModel, Field
from typing import Optional, List

class Movie(BaseModel):
    #id: Optional[int] = None
    title: str = Field(...,
        min_length=5,
        max_length=15
    )
    overview: str = Field(...,
        min_length=15,
        max_length=55
    )
    year: int = Field(...,
        le=2022
    )
    rating: float = Field(
        ...,
        ge=1,
        le=10
    )
    category: str = Field(
        ...,
        min_length=5,
        max_length=15
    )


    class Config:
        schema_extra = {
            "example": {
                #"id": 1,
                "title": "Titulo de exmp",
                "overview": "Esto es una descripcion de mas de 15",
                "year": 2022,
                "rating": 9.8,
                "category": "Accion",

            }
        }
