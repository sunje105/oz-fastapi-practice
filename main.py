from fastapi import FastAPI, Path, HTTPException, Query, Body, status
from schema import UserSignupRequest, UserResponse, UserUpdateRequest
from sqlalchemy import select
from typing import List, Optional
from db_connection import SessionFactory
from models import User

users =[
    {"id": 1, "name": "John Doe", "age": 30},
    {"id": 2, "name": "Jane Doe", "age": 25},
    {"id": 3, "name": "Alice Smith", "age": 28},
    {"id": 4, "name": "Bob Johnson", "age": 35}
]

app = FastAPI()

# @app.get("/hello")
# def root_handler():
#     return hello_world()

# def hello_world():
#     return {"message": "Hello World"}

@app.get(
    "/users", 
    response_model=List[UserResponse], # 리스트 형태로 반환함을 명시
    status_code=status.HTTP_200_OK
)
def get_users():
    with SessionFactory() as session:
        stmt = select(User)
        results = session.execute(stmt)
        users = results.scalars().all()
    return users

# 3. 회원 검색 API (Query Parameter 활용)
@app.get(
    "/users/search", 
    response_model=List[UserResponse], 
    status_code=status.HTTP_200_OK
)
def search_users(
    name: Optional[str] = Query(None, description="Search user by name"),
    min_age: Optional[int] = Query(None, ge=0, description="Minimum age filter")
):
    results = users
    if name:
        results = [u for u in results if name.lower() in u["name"].lower()]
    if min_age:
        results = [u for u in results if u["age"] >= min_age]
    
    return results

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     for u in user:
#         if u["id"] == user_id:
#             return u
#     return {"message": "User not found"}

response_model = UserResponse,

@app.post("/users/signup", 
          status_code=201,
          response_model = UserResponse, 
          description="Create a new user")

def signup_handler(body: UserSignupRequest):
    new_user = User(name=body.name, age=body.age)

    with SessionFactory() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # 새로 생성된 객체의 ID를 가져오기 위해
    # session = SessionFactory()
    # session.add(new_user)
    # session.commit()
    # session.refresh(new_user)  # 새로 생성된 객체의 ID를 가져오기 위해
    # session.close()
    # new_user = {
    #     "id": len(users) + 1,
    #     "name": body.name,
    #     "age": body.age
    # }
    # users.append(new_user)
    return new_user



# --- 5. 회원 정보 수정 (PATCH) ---
@app.patch("/users/{user_id}", 
           response_model=UserResponse, 
           status_code=status.HTTP_200_OK)
def update_user_handler(
    user_id: int = Path(..., ge=1, description="수정할 사용자의 ID"),
    body: UserSignupRequest = Body(..., description="수정할 데이터")
):
    # 실제 사용자 찾기
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 비즈니스 로직 예시: 둘 다 수정하려 할 때 에러 발생 (기존 로직 유지)
    if body.name is not None and body.age is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="이름과 나이를 동시에 수정할 수 없습니다."
        )

    # 데이터 업데이트
    if body.name is not None: user["name"] = body.name
    if body.age is not None: user["age"] = body.age
    
    return user

# 2. 단일 사용자 조회 API (기존 get_user_handler 수정)
@app.get(
    "/users/{user_id}", 
    response_model=UserResponse, 
    status_code=status.HTTP_200_OK
)
def get_user_handler(
    user_id: int = Path(..., ge=1, description="The ID of the user to retrieve")
):
    # 실제 데이터에서 ID로 찾기 (인덱스 방식보다 안전함)
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_handler(user_id: int = Path(..., ge=1, description="삭제할 사용자의 ID")):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = [u for u in users if u["id"] != user_id]
    return None