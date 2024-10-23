from ninja import Schema

class Result(Schema):
    result: str

class Error(Schema):
    status: str
    message: str