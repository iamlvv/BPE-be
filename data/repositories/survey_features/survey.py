from datetime import datetime

from data.models.survey_feature_models.survey_model import Survey_model
from sqlalchemy import and_
from database.db import DatabaseConnector


class Survey:
    @classmethod
    def get_survey_detail(cls, survey_id):
        # get survey detail
        session = DatabaseConnector.get_session()
        try:
            survey = (
                session.query(
                    Survey_model.id,
                    Survey_model.name,
                    Survey_model.description,
                    Survey_model.created_at,
                    Survey_model.is_deleted,
                    Survey_model.start_date,
                    Survey_model.end_date,
                    Survey_model.is_published,
                )
                .filter(
                    Survey_model.id == int(survey_id), Survey_model.is_deleted == False
                )
                .first()
            )
            session.commit()
            if survey is None:
                return None
            return {
                "id": survey[0],
                "name": survey[1],
                "description": survey[2],
                "createdAt": survey[3],
                "isDeleted": survey[4],
                "startDate": survey[5],
                "endDate": survey[6],
                "isPublished": survey[7],
            }
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def create_new_survey(cls, process_version_version):
        # create new survey
        session = DatabaseConnector.get_session()
        try:
            survey = Survey_model(
                name="Survey for Process Version: " + process_version_version,
                description="This is the default description for the survey.",
                process_version_version=process_version_version,
                created_at=datetime.now(),
                is_deleted=False,
                is_published=False,
                survey_url="",
                start_date=None,
                end_date=None,
                allow_duplicate_respondent=False,
                send_result_to_respondent=False,
                ces_weight=1,
                nps_weight=1,
                csat_weight=1,
                domain="general",
            )
            session.add(survey)
            session.commit()
            session.close()
            return {
                "id": survey.id,
                "name": survey.name,
                "description": survey.description,
                # "createdAt": survey.created_at,
                # "isDeleted": survey.is_deleted,
                # "startDate": survey.start_date,
                # "endDate": survey.end_date,
                "isPublished": survey.is_published,
                "processVersionVersion": survey.process_version_version,
            }
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def delete_survey(cls, survey_id):
        session = DatabaseConnector.get_session()
        try:
            survey = (
                session.query(Survey_model)
                .filter(Survey_model.id == survey_id, Survey_model.is_deleted == False)
                .first()
            )
            survey.is_deleted = True
            print(survey)
            session.commit()
            session.close()
            return {"message": "Survey is deleted"}
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def config_survey_general(
        cls,
        survey_id,
        survey_name,
        survey_description,
        nps_weight,
        ces_weight,
        csat_weight,
    ):
        session = DatabaseConnector.get_session()
        try:
            survey = (
                session.query(Survey_model)
                .filter(Survey_model.id == survey_id, Survey_model.is_deleted == False)
                .first()
            )
            if survey_name is not None:
                survey.name = survey_name
            if survey_description is not None:
                survey.description = survey_description
            if nps_weight is not None:
                survey.nps_weight = nps_weight
            if ces_weight is not None:
                survey.ces_weight = ces_weight
            if csat_weight is not None:
                survey.csat_weight = csat_weight
            session.commit()
            return {
                "id": survey.id,
                "name": survey.name,
                "description": survey.description,
                "createdAt": survey.created_at,
                "isDeleted": survey.is_deleted,
                "npsWeight": survey.nps_weight,
                "cesWeight": survey.ces_weight,
                "csatWeight": survey.csat_weight,
            }
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def config_survey_response(
        cls,
        survey_id,
        incomplete_survey_action,
        allow_duplicate_respondent,
        send_result_to_respondent,
        start_date,
        end_date,
    ):
        session = DatabaseConnector.get_session()
        try:
            survey = (
                session.query(Survey_model)
                .filter(Survey_model.id == survey_id, Survey_model.is_deleted == False)
                .first()
            )
            if incomplete_survey_action is not None:
                survey.incomplete_survey_action = incomplete_survey_action
            if allow_duplicate_respondent is not None:
                survey.allow_duplicate_respondent = allow_duplicate_respondent
            if send_result_to_respondent is not None:
                survey.send_result_to_respondent = send_result_to_respondent
            if start_date is not None:
                survey.start_date = start_date
            if end_date is not None:
                survey.end_date = end_date
            session.commit()
            return {
                "id": survey.id,
                "incompleteSurveyAction": survey.incomplete_survey_action,
                "allowDuplicateRespondent": survey.allow_duplicate_respondent,
                "sendResultToRespondent": survey.send_result_to_respondent,
                "startDate": survey.start_date,
                "endDate": survey.end_date,
            }
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def check_if_survey_exists(cls, process_version_version):
        session = DatabaseConnector.get_session()
        try:
            survey = (
                session.query(Survey_model)
                .filter(
                    Survey_model.process_version_version == process_version_version,
                    Survey_model.is_deleted == False,
                )
                .first()
            )
            session.commit()
            if survey is None:
                return None
            return survey.id
        except Exception as e:
            session.rollback()
            raise Exception(e)
