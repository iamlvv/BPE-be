from data.repositories.survey_features.question import Question
from services.survey_service.init_questions import Initialize


class Question_service:
    @classmethod
    def check_if_sample_questions_initialized(cls):
        return Question.check_if_sample_questions_initialized()

    @classmethod
    def initialize_sample_questions(cls):
        check_if_sample_questions_initialized = (
            Question_service.check_if_sample_questions_initialized()
        )
        if check_if_sample_questions_initialized:
            return {"message": "Sample questions are already initialized"}

        Initialize.initialize_questions()
        Initialize.initialize_question_options()
        return "Initialize successfully"
