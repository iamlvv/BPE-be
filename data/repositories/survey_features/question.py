from data.models.survey_feature_models.question_model import Question_model
from database.db import DatabaseConnector


class Question:
    @classmethod
    def get_sample_questions(cls):
        # get list of prepared questions from Question table
        # question is marked prepared if the origin field is "system" and "domain" is "general"
        session = DatabaseConnector.get_session()
        sample_questions_list = (
            session.query(
                Question_model.id,
                Question_model.content,
                Question_model.is_deleted,
                Question_model.question_type,
            )
            .filter(
                Question_model.origin == "system", Question_model.domain == "general"
            )
            .all()
        )
        return sample_questions_list

    @classmethod
    def check_if_sample_questions_initialized(cls):
        # check if sample questions are already initialized
        session = DatabaseConnector.get_session()
        sample_questions_list = (
            session.query(Question_model)
            .filter(
                Question_model.origin == "system", Question_model.domain == "general"
            )
            .all()
        )
        session.commit()
        return len(sample_questions_list) > 0

    @classmethod
    def create_question(cls, content, question_type):
        session = DatabaseConnector.get_session()
        try:
            question = Question_model(
                content=content,
                question_type=question_type,
                origin="user",
                domain="general",
                is_deleted=False,
                contributor_id=None,
                usage_count=0,
            )
            session.add(question)
            session.commit()
            return question
        except Exception as e:
            session.rollback()
            raise Exception(e)


# insert sample questions into table question
# insert sample sections into table section
