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
        targeted_cycle_time,
        worst_cycle_time,
        current_cycle_time,
        targeted_cost,
        worst_cost,
        current_cost,
        targeted_quality,
        worst_quality,
        current_quality,
        targeted_flexibility,
        worst_flexibility,
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
                targeted_cycle_time,
                worst_cycle_time,
                current_cycle_time,
                targeted_cost,
                worst_cost,
                current_cost,
                targeted_quality,
                worst_quality,
                current_quality,
                targeted_flexibility,
                worst_flexibility,
                current_flexibility,
            )
        else:
            process_version_health = cls.add_health_of_active_process_versions(
                process_version_version,
                targeted_cycle_time,
                worst_cycle_time,
                current_cycle_time,
                targeted_cost,
                worst_cost,
                current_cost,
                targeted_quality,
                worst_quality,
                current_quality,
                targeted_flexibility,
                worst_flexibility,
                current_flexibility,
            )
        return {
            "processVersionVersion": process_version_health.process_version_version,
            "targetedCycleTime": process_version_health.targeted_cycle_time,
            "worstCycleTime": process_version_health.worst_cycle_time,
            "currentCycleTime": process_version_health.current_cycle_time,
            "targetedCost": process_version_health.targeted_cost,
            "worstCost": process_version_health.worst_cost,
            "currentCost": process_version_health.current_cost,
            "targetedQuality": process_version_health.targeted_quality,
            "worstQuality": process_version_health.worst_quality,
            "currentQuality": process_version_health.current_quality,
            "targetedFlexibility": process_version_health.targeted_flexibility,
            "worstFlexibility": process_version_health.worst_flexibility,
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
        targeted_cycle_time,
        worst_cycle_time,
        current_cycle_time,
        targeted_cost,
        worst_cost,
        current_cost,
        targeted_quality,
        worst_quality,
        current_quality,
        targeted_flexibility,
        worst_flexibility,
        current_flexibility,
    ):
        return Health.update_health_of_active_process_version(
            process_version_version,
            targeted_cycle_time,
            worst_cycle_time,
            current_cycle_time,
            targeted_cost,
            worst_cost,
            current_cost,
            targeted_quality,
            worst_quality,
            current_quality,
            targeted_flexibility,
            worst_flexibility,
            current_flexibility,
        )

    @classmethod
    def add_health_of_active_process_versions(
        cls,
        process_version_version,
        targeted_cycle_time,
        worst_cycle_time,
        current_cycle_time,
        targeted_cost,
        worst_cost,
        current_cost,
        targeted_quality,
        worst_quality,
        current_quality,
        targeted_flexibility,
        worst_flexibility,
        current_flexibility,
    ):
        return Health.add_health_of_active_process_version(
            process_version_version,
            targeted_cycle_time,
            worst_cycle_time,
            current_cycle_time,
            targeted_cost,
            worst_cost,
            current_cost,
            targeted_quality,
            worst_quality,
            current_quality,
            targeted_flexibility,
            worst_flexibility,
            current_flexibility,
        )

    @classmethod
    def get_health_of_active_process_version(cls, process_version_version):
        health_stats = Health.get_health_of_active_process_version(
            process_version_version
        )
