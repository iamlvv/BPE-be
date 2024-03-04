from data.repositories.survey_features.survey import Survey
from services.project_service.work_on import WorkOnService
from services.survey_service.question_in_section import (
    Question_in_section_service,
)
from services.survey_service.section import Section_service
from services.utils import Permission_check


class Survey_service:
    @classmethod
    def get_survey_detail(cls, survey_id, project_id, user_id):
        # check if user has access to the survey
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        # get survey detail
        return Survey.get_survey_detail(survey_id)

    @classmethod
    def create_new_survey(
        cls,
        project_id,
        user_id,
        survey_name,
        survey_description,
        process_version_version,
    ):
        # check if user has access to the survey
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        # create new survey
        new_survey = Survey.create_new_survey(
            survey_name, survey_description, process_version_version
        )
        # create sections for the survey
        sections_list_in_survey = Section_service.create_sample_sections(
            new_survey["id"]
        )
        # create questions and question options in each section for the survey
        questions_list_in_survey = Question_in_section_service.create_sample_questions(
            sections_list_in_survey
        )
        # return list of sections, questions and question options in the survey
        return {
            "survey": new_survey,
            "sections": sections_list_in_survey,
            "questions": questions_list_in_survey,
        }

    @classmethod
    def get_survey_content(cls, user_id, project_id, survey_id):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        sections_list_in_survey = Section_service.get_sections_in_survey(survey_id)
        print("sections_list_in_survey: ", sections_list_in_survey)
        questions_list_in_survey = Question_in_section_service.get_questions_in_survey(
            sections_list_in_survey
        )
        return {
            "sections": sections_list_in_survey,
            "questions": questions_list_in_survey,
        }

    @classmethod
    def delete_survey(cls, user_id, project_id, survey_id):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        return Survey.delete_survey(survey_id)
