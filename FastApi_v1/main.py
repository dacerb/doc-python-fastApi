#python libs
from typing import Optional
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

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



class loginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel212")
    message: str = "login successfuly"


@app.get(
        path="/",
        status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "world"}


## Request and Response body
## path operation path decoration
@app.post(
    path="/person/new",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the APP"
)  # Path operation decoration

def create_person(person: Person = Body(...)):      # Path operation function
    """
    Create Person

    This path operation create a person in the app and save information in the database.
    :param person:
    - Request Body paramaeters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status.

    :return: A Person Model with first name, last name, age, hair color and marital status.
    """
    return person

@app.post(
    path="/person/new/four",
    response_model=PersonFourOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)  # Path operation decoration
def create_person(person: PersonFour = Body(...)):      # Path operation function
    return person

@app.post(
    path="/person/new/four/fix",
    response_model=PersonFourOutFix,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)  # Path operation decoration
def create_person(person: PersonFourFix = Body(...)):      # Path operation function
    return person



# validaciones query parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
)
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

persons = [1,2,3,4,5]
@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        example=1,
        description="This is the person ID. this valeu greater That 0"

    )
):
    if not person_id in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist."
        )
    return {
        "detail": "it_exist!",
        person_id: person_id
    }



# validaciones: Request body
@app.put(
    path="/person/{person_id}",
    tags=["Persons"]
)
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



@app.put(
    path="/person/two/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
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


@app.put(
    path="/person/three/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
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


@app.put(
    path="/person/four/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
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


@app.post(
    path="/login",
    response_model=loginOut,
    status_code=status.HTTP_200_OK,
    tags=["Logins"]
)
def login(
        username: str = Form(...), password: str = Form(...)
):
    return loginOut(username=username)


## Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
        first_name: str = Form(
            ...,
            max_length=20,
            min_length=1
        ),
        last_name: str = Form(
                ...,
                max_length=20,
                min_length=1
            ),
        email: EmailStr = Form(...),
        message: str = Form(
                ...,
                min_length=20
        ),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/post-image",
    tags=['Images']
)
def post_image(
        image: UploadFile = File(...)
):
    """
    **ACA hay cosas pasa realizar.**
    :param image:
    :return:
    """
    size_file = len(image.file.read())
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(byte)": size_file,  # al leer un archivo podemos pasarla por len para obtener los bites
        "Size(kb)": size_file/1024,  # al leer un archivo podemos pasarla por len para obtener los bites
        "Size(kb round)": round(size_file / 1024),  # al leer un archivo podemos pasarla por len para obtener los bites
        "Size(kb Round c 2 digitos )": round(size_file / 1024, ndigits=2)  # al leer un archivo podemos pasarla por len para obtener los bites
    }

    pass