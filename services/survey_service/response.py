from datetime import datetime

from data.repositories.survey_features.response import Response
from services.survey_service.answer import Answer_service
from services.survey_service.respondent import Respondent_service
from services.survey_service.survey import Survey_service
from services.survey_service.survey_result import Survey_result_service


class Response_service:
    @classmethod
    def submit_survey_form(cls, answers, email, full_name, process_version_version):
        # get survey id from process_version_version
        # add respondent to table Respondent
        # create new response
        # add answers to table Answer. answers is a list of answer objects, each object contains question_id, value
        # calculate scores for the survey
        # return if survey allows respondent to see the result and send another response
        survey_id = Survey_service.check_if_survey_exists(process_version_version)
        # new_respondent = Respondent_service.create_respondent(email, full_name)
        # respondent_id = new_respondent.id
        # end_date = datetime.now()
        # new_response = cls.create_response(
        #     survey_id, respondent_id, end_date, start_date=None
        # )
        # # add answers
        # response_id = new_response.id
        # for answer in answers:
        #     Answer_service.add_answer(
        #         response_id, answer["questionInSectionId"], answer["value"]
        #     )

        # get number of responses
        current_number_of_responses = cls.get_number_of_responses(survey_id)
        # calculate scores
        score = Survey_result_service.calculate_scores(
            survey_id, current_number_of_responses
        )

        # return if survey allows respondent to see the result and send another response
        survey_config = Survey_service.get_survey_response_config_some(survey_id)
        return {
            "message": "Survey form submitted successfully",
            "sendResultToRespondent": survey_config["sendResultToRespondent"],
            "allowDuplicateRespondent": survey_config["allowDuplicateRespondent"],
            "incompleteSurveyAction": survey_config["incompleteSurveyAction"],
            "score": score,
        }

    @classmethod
    def create_response(cls, survey_id, respondent_id, end_date, start_date=None):
        return Response.create_response(survey_id, respondent_id, start_date, end_date)

    @classmethod
    def get_number_of_responses(cls, survey_id):
        return Response.get_number_of_responses(survey_id)
