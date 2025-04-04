from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserList(BaseModel):
    users: list[UserPublic]
