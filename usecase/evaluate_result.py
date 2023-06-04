from models.evaluated_result import EvaluatedResult
from models.work_on import WorkOn


class EvaluatedResultUsercase:
    @classmethod
    def save(self, user_id, xml_file_link, project_id, process_id, name, result, description):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        EvaluatedResult.insert(xml_file_link, project_id, process_id,
                               name, result, description)

    @classmethod
    def get_all_result_by_bpmn_file(self, user_id, project_id, process_id, xml_file_link):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return EvaluatedResult.get_result_by_bpmn_file(xml_file_link, project_id, process_id)

    @classmethod
    def get_result(self, user_id, project_id, process_id, xml_file_link, name):
        if not WorkOn.can_view(user_id, project_id):
            raise Exception("permission denied")
        return EvaluatedResult.get(xml_file_link, project_id, process_id, name)

    @classmethod
    def delete(self, user_id, xml_file_link, project_id, process_id, name):
        if not WorkOn.can_edit(user_id, project_id):
            raise Exception("permission denied")
        EvaluatedResult.delete(xml_file_link, project_id, process_id, name)
