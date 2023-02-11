
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "world"}


## Request and Response body
## path operation path decoration
@app.post("/person/new")  # Path operation decoration
def create_person():      # Path operation function
    return ""