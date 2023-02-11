#python libs
from typing import Optional

# pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query

app = FastAPI()

## models
class Person(BaseModel):
    fist_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None



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
        name: Optional[str] = Query(default=None, min_length=1, max_length=50, regex="^[a-zA-Z]*$", title="nombre de la persona", description="aca pone tu nombre papa"),
        age: int = Query(...)
):
    return {
        name: age
    }

