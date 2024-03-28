from data.repositories.process_portfolio_features.health import Health
from services.utils import Permission_check


class Health_service:
    @classmethod
    def get_health_of_active_process_versions_in_workspace(cls, workspace_id, user_id):
        workspace_owner = Permission_check.check_if_user_is_workspace_owner(
            workspace_id, user_id
        )
        if not workspace_owner:
            raise Exception("permission denied")

    @classmethod
    def edit_health_of_active_process_versions(
        cls,
        workspace_id,
        process_version_version,
        user_id,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        workspace_owner = Permission_check.check_if_user_is_workspace_owner(
            workspace_id, user_id
        )
        if not workspace_owner:
            raise Exception("permission denied")

        # check if process version exists in table Health
        process_version = cls.check_if_process_version_exists_in_health(
            process_version_version
        )
        process_version_health = None
        if process_version:
            process_version_health = cls.update_health_of_active_process_versions(
                process_version_version,
                current_cycle_time,
                current_cost,
                current_quality,
                current_flexibility,
            )
        else:
            process_version_health = cls.add_health_of_active_process_versions(
                process_version_version,
                current_cycle_time,
                current_cost,
                current_quality,
                current_flexibility,
            )
        return {
            "processVersionVersion": process_version_health.process_version_version,
            "currentCycleTime": process_version_health.current_cycle_time,
            "currentCost": process_version_health.current_cost,
            "currentQuality": process_version_health.current_quality,
            "currentFlexibility": process_version_health.current_flexibility,
        }

    @classmethod
    def check_if_process_version_exists_in_health(cls, process_version_version):
        health = Health.check_if_process_version_exists_in_health(
            process_version_version
        )
        if health is None:
            raise Exception("health of process version does not exist")
        return health

    @classmethod
    def update_health_of_active_process_versions(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        return Health.update_health_of_active_process_version(
            process_version_version,
            current_cycle_time,
            current_cost,
            current_quality,
            current_flexibility,
        )

    @classmethod
    def add_health_of_active_process_versions(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        return Health.add_health_of_active_process_version(
            process_version_version,
            current_cycle_time,
            current_cost,
            current_quality,
            current_flexibility,
        )

    @classmethod
    def get_health_of_active_process_version(cls, process_version_version):
        health_stats = Health.get_health_of_active_process_version(
            process_version_version
        )
