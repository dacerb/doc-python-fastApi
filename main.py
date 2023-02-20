#python libs
from typing import Optional
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"



## MODELS

# cargando los ejemplos en la definicion
class PersonBase(BaseModel):
    fist_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="david"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="qweqweqweqwe"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=66
    )
    hair_color: Optional[HairColor] = Field(default=None, example="red")
    is_married: Optional[bool] = Field(default=None, example=False)
class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
    )
class PersonOut(PersonBase):
   pass
class Locations(BaseModel):
    city: str
    state: str
    country: str



###  ENDPOINTS
@app.get("/")
def home():
    return {"Hello": "world"}


## Request and Response body
## path operation path decoration
@app.post("/person/new")  # Path operation decoration
def create_person(person: Person = Body(...)):      # Path operation function
    return person



# validaciones query parameters
@app.get('/person/detail')
def show_person(
        name: Optional[str] = Query(
            default=None,
            min_length=1,
            max_length=50,
            regex="^[a-zA-Z]*$",
            title="Person Name",
            description="This is the person name. It's between 1 and 50 characters",
            example="martin"
        ),
        age: int = Query(
            ...,
            title="Person Age",
            description="This is the person age. It's required",
            example=23
        )
):
    return {
        name: age
    }


# validaciones query parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID. this valeu greater That 0",
        example=123
    )
):
    return {
        "detail": "it_exist!",
        person_id: person_id
    }



# validaciones: Request body



@app.put("/person/{person_id}", response_model=PersonOut)
def update_person(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=124
    ),
    person: Person = Body(
        ...,
    ),
    locations: Locations = Body(
        ...,
    )
):
    results = person.dict()
    results.update(locations.dict())
    return results
