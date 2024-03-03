from data.repositories.survey_features.question_option import Question_option
from data.repositories.survey_features.question_option_section_mapping import (
    Question_option_section_mapping,
)


class Question_option_service:
    @classmethod
    def create_sample_question_option(cls, questions_list_in_survey):
        # only create question options for multiple choice questions and branching questions
        # they are the first 2 questions in the survey
        question_options = []
        for i in range(0, 2):
            question = questions_list_in_survey[i]
            if question["type"] in ["multiple_choice", "branching"]:
                # create question options
                question_options.append(
                    Question_option.create_sample_question_option(question, i)
                )
                # add question options to the question

        return question_options
