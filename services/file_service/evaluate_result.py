from data.repositories.evaluated_result import EvaluatedResult
from services.project_service.work_on import WorkOnService
from services.survey_service.survey_result import Survey_result_service


class EvaluatedResultService:
    @classmethod
    def save(
        cls,
        user_id,
        xml_file_link,
        project_id,
        process_id,
        name,
        result,
        description,
        version,
    ):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        EvaluatedResult.insert(
            xml_file_link, project_id, process_id, name, result, description, version
        )

    @classmethod
    def get_all_result_by_bpmn_file(
        cls, user_id, project_id, process_id, xml_file_link
    ):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return EvaluatedResult.get_result_by_bpmn_file(
            xml_file_link, project_id, process_id
        )

    @classmethod
    def get_result(cls, user_id, project_id, process_id, xml_file_link, name):
        if not WorkOnService.can_view(user_id, project_id):
            raise Exception("permission denied")
        return EvaluatedResult.get(xml_file_link, project_id, process_id, name)

    @classmethod
    def delete(cls, user_id, xml_file_link, project_id, process_id, name):
        if not WorkOnService.can_edit(user_id, project_id):
            raise Exception("permission denied")
        EvaluatedResult.delete(xml_file_link, project_id, process_id, name)

    @classmethod
    def get_evaluation_result_of_process_version(cls, process_version_version):
        evaluation_result = EvaluatedResult.get_evaluation_result_of_process_version(
            process_version_version
        )

        # result is jsonb
        # extract total cycle time, total cost, total quality, total flexibility from result
        if evaluation_result is None:
            return None
        survey_result = Survey_result_service.get_survey_result(process_version_version)
        print("survey_result", survey_result)
        result = evaluation_result.result[0]
        return {
            "totalCycleTime": result["totalCycleTime"],
            "totalCost": result["totalCost"],
            "totalQuality": (result["quality"] + survey_result["totalScore"]) / 2
            if survey_result is not None
            else None,
            "totalFlexibility": result["flexibility"],
        }
