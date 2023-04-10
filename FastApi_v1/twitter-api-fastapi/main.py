# Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import (
    EmailStr,
    Field
)

# FastAPI
from fastapi import FastAPI
from fastapi import (
    status,
    Body
)

app = FastAPI()

# Models
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UseLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    ## Signup

    #### This path operations register a user in the app.


    - :parameter:
        - Request body:
            - user: UserRegister


    - :return: a Json with the basic user information
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime

    """

    with open("users.json", "r+", encoding="utf-8") as file:
        results_data = json.loads(file.read())

        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results_data.append(user_dict)

        file.seek(0)
        file.write(json.dumps(results_data))

        return user


### Login a users
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

### Show all user
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"]
)
def show_all_users():
    """
        This path operation show all users in the app
        - :parameter:
            -
        - :return:
            - a json list with all users in the app, with the following keys:
                - user_id: UUID
                - email: Emailstr
                - first_name: str
                - last_name: str
                - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as file:
        results_data = json.loads(file.read())

        return  results_data

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass



## Tweets

### Show all Tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
)

def home():
    """
            This path operation show all tweets in the app
            - :parameter:
                -
            - :return:
                - a json list with all tweets in the app, with the following keys:

                    - tweet_id: UUID
                    - content: str
                    - created_at: datetime
                    - updated_at: Optional datetime
                    - by:
                        - user_id: UUID
                        - email: Emailstr
                        - first_name: str
                        - last_name: str
                        - birth_date: datetime
        """
    with open("tweets.json", "r", encoding="utf-8") as file:
        results_data = json.loads(file.read())
        return results_data

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
        ## Post

        #### This path operations post a tweet in the app.


        - :parameter:
            - Request body:
                - tweet: Tweet


        - :return: a Json with the basic user information
            - tweet_id: UUID
            - by: User
            - content: str
            - created_at: datetime
             - updated_at: Optional datetime
    """
    with open("tweets.json", "r+", encoding="utf-8") as file:

        results_data = json.loads(file.read())

        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])

        if tweet_dict.get("updated_at", None):
            tweet_dict['updated_at'] = str(tweet_dict['updated_at'])

        results_data.append(tweet_dict)

        file.seek(0)
        file.write(json.dumps(results_data))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass