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

## models
class Person(BaseModel):
    fist_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class PersonTwo(BaseModel):
    fist_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Locations(BaseModel):
    city: str
    state: str
    country: str



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
            description="This is the person name. It's between 1 and 50 characters"
        ),
        age: int = Query(
            ...,
            title="Person Age",
            description="This is the person age. It's required"
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
        description="This is the person ID. this valeu greater That 0"

    )
):
    return {
        "detail": "it_exist!",
        person_id: person_id
    }



# validaciones: Request body
@app.put("/person/{person_id}")
def update_person(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
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



@app.put("/person/two/{person_id}")
def update_person_two(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: PersonTwo = Body(
        ...,
    ),
    locations: Locations = Body(
        ...,
    )
):
    results = person.dict()
    results.update(locations.dict())

    return results

