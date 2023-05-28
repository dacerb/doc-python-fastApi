from fastapi import Body, APIRouter
from fastapi.responses import JSONResponse
from middlewares.jwt_bearer import create_token
from schemas.user import User

user_router = APIRouter()

@user_router.post(
    path="/login",
    tags=["Auth"],
    status_code=200

)
def login(user: User = Body(...)):

    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)