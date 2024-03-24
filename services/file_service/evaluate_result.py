from data.repositories.evaluated_result import EvaluatedResult
from services.project_service.work_on import WorkOnService


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
