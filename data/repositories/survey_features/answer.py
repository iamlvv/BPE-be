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

    @classmethod
    def get_all_answers(cls, response_id):
        session = DatabaseConnector.get_session()
        try:
            answers = (
                session.query(Answer_model)
                .filter(
                    Answer_model.response_id == response_id,
                    Answer_model.is_deleted == False,
                )
                .all()
            )
            session.commit()
            return answers
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def delete_answers(cls, response_id):
        session = DatabaseConnector.get_session()
        try:
            answers = (
                session.query(Answer_model)
                .filter(
                    Answer_model.response_id == response_id,
                    Answer_model.is_deleted == False,
                )
                .all()
            )
            for answer in answers:
                answer.is_deleted = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(e)
