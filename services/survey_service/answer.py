from data.repositories.survey_features.answer import Answer


class Answer_service:
    @classmethod
    def add_answer(cls, response_id, question_id, value):
        return Answer.create_answer(response_id, question_id, value)
