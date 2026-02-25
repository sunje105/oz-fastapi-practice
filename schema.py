from pydantic import BaseModel

class UserSignupRequest(BaseModel):
    name: str
    age: int | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    age: int | None = None

class UserUpdateRequest(BaseModel):
    name: str | None = None
    age: int | None = None