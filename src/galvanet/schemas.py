from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
