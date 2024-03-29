import hashlib

from data.repositories.constant import Role
from data.repositories.workspace import Workspace
from services.project_service.work_on import WorkOnService

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

    @classmethod
    def compare_permission(
        cls, user_id_and_project_roles_list, member_id_and_workspace_permission_list
    ):
        # each parameter is a dict with 2 keys: user_id and role, each key is a list
        # return true if all user_id in user_id_and_project_roles_list has role that is higher or equal to in
        # member_id_and_workspace_permission_list
        for user in user_id_and_project_roles_list:
            for member in member_id_and_workspace_permission_list:
                if user["user_id"] == member["user_id"]:
                    if user["role"] > PermissionConverter.convert_permission_to_role(
                        member["permission"]
                    ):
                        return False

        return True


class Permission_check:
    @classmethod
    def check_user_has_access_survey(cls, project_id, user_id):
        return WorkOnService.is_project_owner(user_id, project_id)

    @classmethod
    def check_if_user_is_workspace_owner(cls, workspace_id, user_id):
        return Workspace.check_if_user_is_workspace_owner(workspace_id, user_id)
