from services.utils import Permission_check


class Health_service:
    @classmethod
    def get_health_of_active_process_versions_in_workspace(cls, workspace_id, user_id):
        workspace_owner = Permission_check.check_if_user_is_workspace_owner(
            workspace_id, user_id
        )
        if not workspace_owner:
            raise Exception("permission denied")
