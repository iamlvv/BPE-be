from data.models.survey_feature_models.question_model import (
    Question_in_section_model,
)
from data.repositories.survey_features.question_option import Question_option
from database.db import DatabaseConnector
from services.survey_service.init_question_data import init_questions


class Question_in_section:
    @classmethod
    def create_question_in_section(
        cls, section_id, sample_question, current_order_in_section
    ):
        session = DatabaseConnector.get_session()
        try:
            question_in_section = Question_in_section_model(
                section_id=section_id,
                question_id=sample_question.id,
                content=sample_question.content,
                is_deleted=sample_question.is_deleted,
                is_required=True,
                order_in_section=init_questions[current_order_in_section][
                    "order_in_section"
                ],
                weight=init_questions[current_order_in_section]["weight"],
                question_type=init_questions[current_order_in_section]["question_type"],
            )
            session.add(question_in_section)
            session.commit()
            session.close()
            return question_in_section
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def get_questions_in_survey(cls, sections_list_in_survey):
        session = DatabaseConnector.get_session()
        try:
            questions_in_survey = []
            # get questions in each section, but with multiple choice and branching questions,
            # query question_option table to get options for each question
            # group them by section
            # get question_options for first two question
            question_options_list = []
            for section in sections_list_in_survey:
                questions_in_section = (
                    session.query(Question_in_section_model)
                    .filter(Question_in_section_model.section_id == section["id"])
                    .order_by(Question_in_section_model.order_in_section)
                    .all()
                )
                # only get question options for multiple choice and branching questions
                for question in questions_in_section:
                    if question.question_type in ["multiple_choice", "branching"]:
                        question_options = (
                            Question_option.get_question_options_in_question_in_section(
                                question.id
                            )
                        )
                        question_options_list.append(question_options)

                questions_in_survey.append(
                    {
                        "section_id": section["id"],
                        "section_name": section["name"],
                        "questions": [
                            {
                                "question_options": (
                                    [
                                        {
                                            "id": question_option_item[0],
                                            "content": question_option_item[1],
                                            "order_in_question": question_option_item[
                                                2
                                            ],
                                        }
                                        for question_option in question_options_list
                                        for question_option_item in question_option
                                        if question_option_item[3] == question.id
                                    ]
                                    if question.question_type
                                    in ["multiple_choice", "branching"]
                                    else []
                                ),
                                "id": question.id,
                                "content": question.content,
                                "is_deleted": question.is_deleted,
                                "is_required": question.is_required,
                                "order_in_section": question.order_in_section,
                                "weight": question.weight,
                                "question_type": question.question_type,
                            }
                            for question in questions_in_section
                        ],
                    }
                )
            session.close()
            return questions_in_survey
        except Exception as e:
            session.rollback()
            raise Exception(e)
