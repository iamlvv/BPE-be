import jwt
import os


def encode(payload):
    return jwt.encode(payload, os.environ.get("SECRET"), algorithm="HS256")


def decode(jwt_string):
    return jwt.decode(jwt_string, os.environ.get("SECRET"), algorithms="HS256")


def get_id_from_token(jwt_string):
    result = jwt.decode(jwt_string, os.environ.get(
        "SECRET"), algorithms="HS256")
    return result["id"]
