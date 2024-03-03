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
            if len(survey) == 0:
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
    def create_new_survey(
        cls, survey_name, survey_description, process_version_version
    ):
        # create new survey
        session = DatabaseConnector.get_session()
        try:
            survey = Survey_model(
                name=survey_name,
                description=survey_description,
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
                "createdAt": survey.created_at,
                "isDeleted": survey.is_deleted,
                "startDate": survey.start_date,
                "endDate": survey.end_date,
                "isPublished": survey.is_published,
                "processVersionVersion": survey.process_version_version,
            }
        except Exception as e:
            session.rollback()
            raise Exception(e)
