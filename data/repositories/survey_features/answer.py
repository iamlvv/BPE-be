from data.models.survey_feature_models.answer_model import Answer_model
from database.db import DatabaseConnector


class Answer:
    @classmethod
    def create_answer(cls, response_id, question_id, value):
        session = DatabaseConnector.get_session()
        try:
            answer = Answer_model(
                response_id=response_id,
                question_id=question_id,
                value=value,
                is_deleted=False,
            )
            session.add(answer)
            session.commit()
            return answer
        except Exception as e:
            session.rollback()
            raise Exception(e)
