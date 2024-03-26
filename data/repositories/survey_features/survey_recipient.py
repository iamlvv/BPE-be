from data.models.survey_feature_models.survey_model import (
    Survey_recipient_model,
    Survey_recipient_association_model,
)
from database.db import DatabaseConnector


class Survey_send:
    @classmethod
    def save_survey_recipient_email(cls, survey_id, recipient_id):
        session = DatabaseConnector.get_session()
        try:
            survey_recipient = Survey_recipient_association_model(
                survey_id=survey_id, survey_recipient_id=recipient_id
            )
            session.add(survey_recipient)
            session.commit()
            return survey_recipient
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def get_survey_recipient_email(cls, survey_id):
        session = DatabaseConnector.get_session()
        try:
            survey_recipient = (
                session.query(Survey_recipient_model)
                .join(
                    Survey_recipient_association_model,
                    Survey_recipient_model.id
                    == Survey_recipient_association_model.survey_recipient_id,
                )
                .filter(
                    Survey_recipient_association_model.survey_id == survey_id,
                )
                .all()
            )
            session.commit()
            return survey_recipient
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def delete_survey_recipient_email(cls, survey_id, recipient_id):
        session = DatabaseConnector.get_session()
        try:
            survey_recipient = (
                session.query(Survey_recipient_association_model)
                .filter(
                    Survey_recipient_association_model.survey_id == survey_id,
                    Survey_recipient_association_model.survey_recipient_id
                    == recipient_id,
                )
                .delete()
            )
            session.commit()
            return survey_recipient
        except Exception as e:
            session.rollback()
            raise Exception(e)


class Survey_recipient:
    @classmethod
    def save_recipient_email(cls, email):
        session = DatabaseConnector.get_session()
        try:
            recipient = Survey_recipient_model(email=email)
            session.add(recipient)
            session.commit()
            return recipient
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def check_if_email_exists(cls, email):
        session = DatabaseConnector.get_session()
        try:
            email = (
                session.query(Survey_recipient_model)
                .filter(Survey_recipient_model.email == email)
                .first()
            )
            session.commit()
            return email
        except Exception as e:
            session.rollback()
            raise Exception(e)


#
