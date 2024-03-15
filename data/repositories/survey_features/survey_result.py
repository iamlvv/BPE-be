from data.models.survey_feature_models.answer_model import Answer_model
from data.models.survey_feature_models.question_model import (
    Section_model,
    Question_in_section_model,
)
from database.db import DatabaseConnector


class Survey_result:
    @classmethod
    def calculate_scores(cls, response_id):
        pass

    @classmethod
    def get_list_of_weight_of_ces_questions(cls, survey_id):
        session = DatabaseConnector.get_session()
        try:
            # get all questions in all sections belong to survey_id
            # join question and section
            list_weight_questions_and_answers = (
                session.query(
                    Question_in_section_model.id,
                    Answer_model.value,
                    Question_in_section_model.weight,
                )
                .join(
                    Question_in_section_model,
                    Question_in_section_model.id == Answer_model.question_id,
                )
                .join(
                    Section_model,
                    Question_in_section_model.section_id == Section_model.id,
                )
                .filter(
                    Section_model.survey_id == survey_id,
                    Question_in_section_model.question_type == "ces",
                    Question_in_section_model.is_deleted == False,
                    Section_model.is_deleted == False,
                )
                .all()
            )
            session.commit()
            return [
                {
                    "question_id": item.id,
                    "value": item.value,
                    "weight": item.weight,
                }
                for item in list_weight_questions_and_answers
            ]
        except Exception as e:
            session.rollback()
            raise Exception(e)
