from data.repositories.survey_features.answer import Answer


class Answer_service:
    @classmethod
    def add_answer(cls, response_id, question_id, value):
        return Answer.create_answer(response_id, question_id, value)

    @classmethod
    def get_all_answers(cls, response_id):
        return Answer.get_all_answers(response_id)

    @classmethod
    def delete_answers(cls, response_id):
        return Answer.delete_answers(response_id)
