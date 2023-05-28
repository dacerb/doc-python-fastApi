from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from middlewares.jwt_bearer import create_token


user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email":"admin@mail.com",
                "password": "admin"
            }
        }

@user_router.post(
    path="/login",
    tags=["Auth"],
    status_code=200

)
def login(user: User = Body(...)):

    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)