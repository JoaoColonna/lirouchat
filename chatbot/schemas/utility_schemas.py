from ninja import Schema

class Result(Schema):
    status: str
    result: str

class Error(Schema):
    status: str
    message: str