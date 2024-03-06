from data.repositories.survey_features.survey import Survey
from services.survey_service.question_in_section import (
    Question_in_section_service,
)
from services.survey_service.section import Section_service
from services.utils import Permission_check


class Survey_service:
    @classmethod
    def get_survey_detail(cls, process_version_version, project_id, user_id):
        # check if user has access to the survey
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        # get survey detail
        return Survey.get_survey_detail(process_version_version)

    @classmethod
    def create_new_survey(
        cls,
        project_id,
        user_id,
        process_version_version,
    ):
        # check if user has access to the survey
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        # create new survey with default name and description
        # default name is: "Survey for process version: {process_version_version}"

        new_survey = Survey.create_new_survey(process_version_version)
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
    def get_survey_content(cls, user_id, project_id, process_version_version):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}
        survey_info = Survey.get_survey_detail(process_version_version)
        if survey_info is None:
            return {"message": "Survey does not exist."}
        survey_id = survey_info["id"]
        sections_list_in_survey = Section_service.get_sections_in_survey(survey_id)
        print("sections_list_in_survey: ", sections_list_in_survey)
        questions_list_in_survey = Question_in_section_service.get_questions_in_survey(
            sections_list_in_survey
        )
        return {
            # "sections": sections_list_in_survey,
            "survey": survey_info,
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

    @classmethod
    def config_survey_general(
        cls,
        survey_id,
        user_id,
        project_id,
        survey_name=None,
        survey_description=None,
        nps_weight=None,
        ces_weight=None,
        csat_weight=None,
    ):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        return Survey.config_survey_general(
            survey_id,
            survey_name,
            survey_description,
            nps_weight,
            ces_weight,
            csat_weight,
        )

    @classmethod
    def config_survey_response(
        cls,
        survey_id,
        user_id,
        project_id,
        incomplete_survey_action=None,
        allow_duplicate_respondent=None,
        send_result_to_respondent=None,
        start_date=None,
        end_date=None,
    ):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        return Survey.config_survey_response(
            survey_id,
            incomplete_survey_action,
            allow_duplicate_respondent,
            send_result_to_respondent,
            start_date,
            end_date,
        )

    @classmethod
    def check_if_survey_exists(cls, process_version_version):
        return Survey.check_if_survey_exists(process_version_version)
