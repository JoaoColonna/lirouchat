from ninja import Schema

class UserSchema(Schema):
    id: int
    username: str 
    email: str
    age: int = None

class UserCreateSchema(Schema):
    username: str
    password: str
    email: str
    age: int = None

class UserUpdateSchema(Schema):
    username: str
    email: str
    age: int = None

