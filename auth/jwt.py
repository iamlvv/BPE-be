import jwt
import os
from models.user import User


def encode(payload):
    return jwt.encode(payload, os.environ.get("SECRET"), algorithm="HS256")


def decode(jwt_string):
    return jwt.decode(jwt_string, os.environ.get("SECRET"), algorithms="HS256")


def verify_token(inp):
    id = inp["id"]
    email = inp["email"]
    User.verify_token(id, email)


def get_id_from_token(jwt_string):
    result = jwt.decode(jwt_string, os.environ.get(
        "SECRET"), algorithms="HS256")
    verify_token(result)
    return result["id"]


def get_email_from_token(jwt_string):
    result = jwt.decode(jwt_string, os.environ.get(
        "SECRET"), algorithms="HS256")
    verify_token(result)
    return result["email"]
