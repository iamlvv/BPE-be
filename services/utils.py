import hashlib

from data.repositories.constant import Role

mySalt = "$2b$12$6rMnsklapuHBKL."


def hash_password(password: str):
    pwd_hash = hashlib.sha256((password + mySalt).encode("utf-8"))
    return pwd_hash.hexdigest()


class PermissionConverter:
    @classmethod
    def convert_permission_to_role(cls, permission):
        if permission == "viewer":
            return Role.CAN_VIEW.value
        elif permission == "sharer":
            return Role.CAN_SHARE.value
        elif permission == "editor":
            return Role.CAN_EDIT.value
        else:
            return Role.OWNER.value

    @classmethod
    def convert_role_to_permission(cls, role):
        if role == Role.CAN_VIEW.value:
            return "viewer"
        elif role == Role.CAN_SHARE.value:
            return "sharer"
        elif role == Role.CAN_EDIT.value:
            return "editor"
        else:
            return "owner"
