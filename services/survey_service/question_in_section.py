from data.repositories.survey_features.question import Question
from data.repositories.survey_features.question_in_section import Question_in_section
from data.repositories.survey_features.question_option import Question_option
from services.survey_service.question_option import Question_option_service
from services.survey_service.question_option_section_mapping import (
    Question_option_section_mapping_service,
)
from services.survey_service.section import Section_service


class Question_in_section_service:
    @classmethod
    def create_sample_questions(cls, sections_list_in_survey):
        # get list of prepared questions from Question table
        sample_questions_list = Question.get_sample_questions()
        # then add each question to the section, order of them in section, weight, etc.
        # for the first section, add 2 first questions
        # for the second section, add questions 3 - 10
        # for the third section, add questions 11 - 14
        # for the fourth section, add question 15
        print("sections_list_in_survey: ", sections_list_in_survey)
        print("sample_questions_list: ", sample_questions_list)
        for section in sections_list_in_survey:
            if section["name"] == "Section 0":
                for j in range(0, 1):
                    # add question to the section
                    question_in_section = (
                        Question_in_section.create_question_in_section(
                            section["id"], sample_questions_list[j], j
                        )
                    )
                    # add question options to the question
                    question_options = Question_option.create_sample_question_option(
                        question_in_section, j
                    )
                    # for this branching question, create a sample mapping of question options to the next sections
                    question_options_section_mapping = Question_option_section_mapping_service.create_sample_question_option_section_mapping(
                        question_options, sections_list_in_survey
                    )

            elif section["name"] == "Section 1":
                for j in range(1, 10):
                    # add question to the section
                    question_in_section = (
                        Question_in_section.create_question_in_section(
                            section["id"], sample_questions_list[j], j
                        )
                    )
                    if sample_questions_list[j][3] in [
                        "multiple_choice",
                        "branching",
                    ]:
                        # add question options to the question
                        Question_option.create_sample_question_option(
                            question_in_section, j
                        )

            elif section["name"] == "Section 2":
                for j in range(10, 14):
                    # add question to the section
                    Question_in_section.create_question_in_section(
                        section["id"], sample_questions_list[j], j
                    )

            elif section["name"] == "Section 3":
                Question_in_section.create_question_in_section(
                    section["id"], sample_questions_list[14], 14
                )
                # add question to the section

                # add order of them in section, weight, etc.
        # then return the list of questions in the survey
        return Question_in_section.get_questions_in_survey(sections_list_in_survey)
