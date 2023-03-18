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

class PersonThree(BaseModel):
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

    class Config:
        schema_extra = {
            "example": {
                "fist_name": "david",
                "last_name": "XS",
                "age": 21,
                "hair_color": "white",
                "is_married": False
            }
        }

# cargando los ejemplos en la definicion
class PersonFour(BaseModel):
    fist_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=""
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=""
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=66
    )
    hair_color: Optional[HairColor] = Field(default=None, example="red")
    is_married: Optional[bool] = Field(default=None, example=False)
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "fist_name": "dav_cfg",
                "last_name": "XS",
                "age": 21,
                "hair_color": "white",
                "is_married": False,
                "password": "falso 123"
            }
        }


class PersonFourOut(BaseModel):
    """
    Clase definida para output para quietar la pass asi no mostramos ese dato
    """
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


class PersonFix(BaseModel):
    fist_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=""
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example=""
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=66
    )
    hair_color: Optional[HairColor] = Field(default=None, example="red")
    is_married: Optional[bool] = Field(default=None, example=False)

class PersonFourFix(PersonFix):
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "fist_name": "dav_cfg",
                "last_name": "XS",
                "age": 21,
                "hair_color": "white",
                "is_married": False,
                "password": "falso 123"
            }
        }
class PersonFourOutFix(PersonFix):
    pass

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

@app.post("/person/new/four", response_model=PersonFourOut)  # Path operation decoration
def create_person(person: PersonFour = Body(...)):      # Path operation function
    return person

@app.post("/person/new/four/fix", response_model=PersonFourOutFix)  # Path operation decoration
def create_person(person: PersonFourFix = Body(...)):      # Path operation function
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


@app.put("/person/three/{person_id}")
def update_person_three(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: PersonThree = Body(
        ...,
    )
):
    results = person.dict()
    return results


@app.put("/person/four/{person_id}")
def update_person_four(

    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: PersonFour = Body(
        ...,
    )
):
    results = person.dict()
    return results
