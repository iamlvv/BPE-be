from datetime import datetime

from data.repositories.survey_features.question_option import Question_option
from data.repositories.survey_features.survey import Survey
from services.survey_service.answer import Answer_service
from services.survey_service.question_in_section import (
    Question_in_section_service,
)
from services.survey_service.question_option import Question_option_service
from services.survey_service.response import Response_service
from services.survey_service.section import Section_service
from services.utils import Permission_check
from smtp.email import Email


class Survey_service:
    @classmethod
    def validate_start_date_end_date(cls, start_date, end_date):
        if start_date is not None and start_date < datetime.now():
            return {"message": "Start date must be in the future"}
        if end_date is not None and end_date < datetime.now():
            return {"message": "End date must be in the future"}
        if start_date is not None and end_date is not None and start_date > end_date:
            return {"message": "Start date must be before end date"}
        return None

    @classmethod
    def get_survey_detail(cls, process_version_version, project_id, user_id):
        # check if user has access to the survey
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            raise Exception("User has no access to the survey")
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
            raise Exception("User has no access to the survey")
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
            raise Exception("User has no access to the survey")
        survey_info = Survey.get_survey_detail(process_version_version)
        if survey_info is None:
            return {"message": "Survey does not exist."}
        survey_id = survey_info["id"]
        sections_list_in_survey = Section_service.get_sections_in_survey(survey_id)
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
            raise Exception("User has no access to the survey")

        # delete all responses
        deleted_responses = Response_service.delete_responses(survey_id)
        # delete all sections
        deleted_sections = Section_service.delete_sections(survey_id)
        # delete all questions
        for section in deleted_sections:
            deleted_questions = Question_in_section_service.delete_questions_in_section(
                section["id"]
            )
            for question in deleted_questions:
                if question["question_type"] in ["multiple_choice", "branching"]:
                    # delete all question options
                    Question_option_service.delete_question_options(question["id"])
        # delete all answers
        for response in deleted_responses:
            Answer_service.delete_answers(response["id"])

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
            raise Exception("User has no access to the survey")

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
            raise Exception("User has no access to the survey")

        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return {"message": "Start date must be before end date"}
            if start_date < datetime.now():
                return {"message": "Start date must be in the future"}
            if end_date < datetime.now():
                return {"message": "End date must be in the future"}
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

    @classmethod
    def get_survey_general_config(cls, survey_id, user_id, project_id):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            raise Exception("User has no access to the survey")
        return Survey.get_survey_general_config(survey_id)

    @classmethod
    def get_survey_response_config(cls, survey_id, user_id, project_id):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            raise Exception("User has no access to the survey")

        return Survey.get_survey_response_config(survey_id)

    @classmethod
    def get_survey_questions_by_section_id(cls, section_id):
        questions_in_section = Question_in_section_service.get_questions_in_section(
            section_id
        )
        question_options_list = []
        for question in questions_in_section:
            if question.question_type in ["multiple_choice", "branching"]:
                question_options = (
                    Question_option.get_question_options_in_question_in_section(
                        question.id
                    )
                )
                question_options_list.append(question_options)
        return {
            "sectionId": int(section_id),
            "questions": [
                {
                    "questionOptions": (
                        [
                            {
                                "id": question_option_item[0],
                                "content": question_option_item[1],
                                "orderInQuestion": question_option_item[2],
                            }
                            for question_option in question_options_list
                            for question_option_item in question_option
                            if question_option_item[3] == question.id
                        ]
                        if question.question_type in ["multiple_choice", "branching"]
                        else []
                    ),
                    "id": question.id,
                    "content": question.content,
                    "isDeleted": question.is_deleted,
                    "isRequired": question.is_required,
                    "orderInSection": question.order_in_section,
                    "questionType": question.question_type,
                }
                for question in questions_in_section
            ],
        }

    @classmethod
    def get_sections_in_survey(cls, process_version_version, mode=None):
        survey = Survey.check_if_survey_exists(process_version_version)
        if survey is None:
            raise Exception("Survey does not exist.")
        if survey.is_published is False and mode == "published":
            raise Exception("Survey is not published.")
        survey_id = survey.id
        sections_list_in_survey = Section_service.get_sections_in_survey(survey_id)
        return {
            "survey": {
                "id": survey_id,
                "name": survey.name,
                "description": survey.description,
            },
            "sections": sections_list_in_survey,
        }

    @classmethod
    def get_survey_response_config_some(cls, survey_id):
        return Survey.get_survey_response_config_some(survey_id)

    @classmethod
    def publish_survey(
        cls,
        process_version_version,
        project_id,
        user_id,
        survey_url,
        email=None,
        start_date=None,
        end_date=None,
    ):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            raise Exception("User has no access to the survey")

        survey = cls.check_if_survey_exists(process_version_version)
        if survey is None:
            raise Exception("Survey does not exist.")
        survey_id = survey.id
        date_validation = cls.validate_start_date_end_date(start_date, end_date)
        if date_validation is not None:
            return date_validation
        # if start date and end date are not provided, use the current date as start date. End date is None

        if start_date is None:
            start_date = datetime.now()

        # send survey url to the email
        if email is not None:
            cls.send_survey_url(email, survey_url, start_date, end_date)
        # update end date and start date of the survey
        return Survey.publish_survey(survey_id, start_date, end_date, survey_url)

    @classmethod
    def send_survey_url(cls, email, survey_url, start_date=None, end_date=None):
        try:
            return Email.send_survey_url(email, survey_url, start_date, end_date)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def close_publish_survey(cls, user_id, project_id, process_version_version):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            raise Exception("User has no access to the survey")

        survey = Survey.check_if_survey_exists(process_version_version)
        if survey is None:
            return {"message": "Survey does not exist."}
        end_date = datetime.now()
        return Survey.close_publish_survey(survey.id, end_date)
