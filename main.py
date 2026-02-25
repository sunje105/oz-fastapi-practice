from fastapi import FastAPI, Path

users =[
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Doe"},
    {"id": 3, "name": "Alice Smith"},
    {"id": 4, "name": "Bob Johnson"}
]

app = FastAPI()

@app.get("/hello")
def root_handler():
    return hello_world()

def hello_world():
    return {"message": "Hello World"}

@app.get("/users")
def get_users():
    return users

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     for u in user:
#         if u["id"] == user_id:
#             return u
#     return {"message": "User not found"}

@app.post("/users/signup")
def signup_user(name: str):
    new_id = max(u["id"] for u in users) + 1
    new_user = {"id": new_id, "name": name}
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}")
def get_user_handler(user_id: int = Path(..., ge=1, description="The ID of the user to retrieve")):
    return users[user_id - 1] if 0 < user_id <= len(users) else {"message": "User not found"}

#GET /items/{item_name}
#item_name: str & max_length 6
items = [
    {"id": 1, "name": "apple"},
    {"id": 2, "name": "banana"},
    {"id": 3, "name": "cherry"},
    {"id": 4, "name": "orange"}
]
@app.get("/items/{item_name}")
def get_item(item_name: str = Path(..., max_length=6, description="The name of the item to retrieve")):
    for item in items:
        if item["name"] == item_name:
            return item
    return {"message": "Item not found"}