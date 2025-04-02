from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
