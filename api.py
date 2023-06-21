import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orm import UserCRUD, UserDomain

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# instalar pip install "uvicorn[standard]"
#sobre directorio raiz de tu proyecto
#uvicorn api:app --reload

userCRUD = UserCRUD()

# Create user
@app.post("/users/")
async def create_user(user_input_data_contract: dict):
    user_input = {
        "name": user_input_data_contract["name"],
        "age": user_input_data_contract["age"]
    }
    user = UserDomain(**user_input).to_user()
    userCRUD.create(user)
    return user

# Get all users
@app.get("/users/")
async def get_users():
    users = userCRUD.read_all()
    return users
# Get single user
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = userCRUD.read(user_id)
    return user

# Update user
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_input_data_contract: dict):
    user_searched = userCRUD.read(user_id)
    user_searched.name = user_input_data_contract["name"]
    user_searched.age = user_input_data_contract["age"]
    userCRUD.update(user_id, user_searched)
    return {"message": "User updated"}

# Delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    userCRUD.delete(user_id)
    return {"message": "User deleted"}