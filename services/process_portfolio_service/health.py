from data.repositories.process_portfolio_features.health import Health
from services.file_service.evaluate_result import EvaluatedResultService
from services.survey_service.survey_result import Survey_result_service
from services.utils import Permission_check
from services.workspace_service.workspace import WorkspaceService


class Health_service:
    @classmethod
    def get_health_of_active_process_versions_in_workspace(cls, workspace_id, user_id):
        workspace_owner = Permission_check.check_if_user_is_workspace_owner(
            workspace_id, user_id
        )
        if not workspace_owner:
            raise Exception("permission denied")

    @classmethod
    def edit_health_of_process_version(
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
            process_version_health = cls.update_health_of_process_version(
                process_version_version,
                current_cycle_time,
                current_cost,
                current_quality,
                current_flexibility,
            )
        else:
            process_version_health = cls.add_health_of_process_version(
                process_version_version,
                current_cycle_time,
                current_cost,
                current_quality,
                current_flexibility,
            )
        return process_version_health

    @classmethod
    def check_if_process_version_exists_in_health(cls, process_version_version):
        health = Health.check_if_process_version_exists_in_health(
            process_version_version
        )
        return health

    @classmethod
    def update_health_of_process_version(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        return Health.update_health_of_process_version(
            process_version_version,
            current_cycle_time,
            current_cost,
            current_quality,
            current_flexibility,
        )

    @classmethod
    def add_health_of_process_version(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        return Health.add_health_of_process_version(
            process_version_version,
            current_cycle_time,
            current_cost,
            current_quality,
            current_flexibility,
        )

    @classmethod
    def get_health_of_process_version(cls, process_version_version):
        health_stats = Health.get_health_of_process_version(process_version_version)
        return health_stats

    @classmethod
    def calculate_total_score(cls, workspace_id, user_id, process_version_version):
        # get evaluation result, which is threshold values for each health metric
        # get workspace measurements as target and worst values
        # get survey result as the external quality of the process
        # calculate score for each metric using pl method
        print("process_version_version", process_version_version)
        evaluation_result = cls.get_evaluation_result_of_process_version(
            process_version_version
        )
        workspace_measurements = cls.get_workspace_measurements(workspace_id, user_id)
        process_version_measurements = cls.get_health_of_process_version(
            process_version_version
        )
        if (
            evaluation_result is None
            or workspace_measurements is None
            or process_version_measurements is None
        ):
            cls.save_total_score(process_version_version, None)
            return
        print(
            "None ",
            evaluation_result,
            workspace_measurements,
            process_version_measurements,
        )
        check = cls.check_values(
            evaluation_result, workspace_measurements, process_version_measurements
        )
        if check is None:
            cls.save_total_score(process_version_version, None)
            return
        cycle_time_score = cls.pl_method(
            workspace_measurements["targetedCycleTime"],
            workspace_measurements["worstCycleTime"],
            process_version_measurements.current_cycle_time,
            evaluation_result["totalCycleTime"],
        )
        cost_score = cls.pl_method(
            workspace_measurements["targetedCost"],
            workspace_measurements["worstCost"],
            process_version_measurements.current_cost,
            evaluation_result["totalCost"],
        )
        quality_score = cls.pl_method(
            workspace_measurements["targetedQuality"],
            workspace_measurements["worstQuality"],
            process_version_measurements.current_quality,
            evaluation_result["totalQuality"],
        )
        flexibility_score = cls.pl_method(
            workspace_measurements["targetedFlexibility"],
            workspace_measurements["worstFlexibility"],
            process_version_measurements.current_flexibility,
            evaluation_result["totalFlexibility"],
        )
        total_score = (
            cycle_time_score + cost_score + quality_score + flexibility_score
        ) / 4
        # save in database
        cls.save_total_score(process_version_version, total_score)

    @classmethod
    def pl_method(cls, target, worst, current, threshold):
        if current >= threshold:
            return abs(current - threshold) / abs(target - threshold)
        return -abs(current - threshold) / abs(threshold - worst)

    @classmethod
    def get_evaluation_result_of_process_version(cls, process_version_version):
        evaluation_result = (
            EvaluatedResultService.get_evaluation_result_of_process_version(
                process_version_version
            )
        )
        return evaluation_result

    @classmethod
    def get_workspace_measurements(cls, workspace_id, user_id):
        return WorkspaceService.get_workspace_measurements(workspace_id, user_id)

    @classmethod
    def check_values(
        cls, evaluation_result, workspace_measurements, process_version_measurements
    ):
        if evaluation_result:
            if evaluation_result["totalCycleTime"] is None:
                return None
            if evaluation_result["totalCost"] is None:
                return None
            if evaluation_result["totalQuality"] is None:
                return None
            if evaluation_result["totalFlexibility"] is None:
                return None

        if workspace_measurements:
            if workspace_measurements["targetedCycleTime"] is None:
                return None
            if workspace_measurements["worstCycleTime"] is None:
                return None
            if workspace_measurements["targetedCost"] is None:
                return None
            if workspace_measurements["worstCost"] is None:
                return None
            if workspace_measurements["targetedQuality"] is None:
                return None
            if workspace_measurements["worstQuality"] is None:
                return None
            if workspace_measurements["targetedFlexibility"] is None:
                return None
            if workspace_measurements["worstFlexibility"] is None:
                return None

        if process_version_measurements:
            if process_version_measurements.current_cycle_time is None:
                return None
            if process_version_measurements.current_cost is None:
                return None
            if process_version_measurements.current_quality is None:
                return None
            if process_version_measurements.current_flexibility is None:
                return None
        return True

    @classmethod
    def save_total_score(cls, process_version_version, total_score):
        return Health.save_total_score(process_version_version, total_score)

    @classmethod
    def get_external_quality_of_process_version(cls, process_version_version):
        return Survey_result_service.get_survey_result(process_version_version)
