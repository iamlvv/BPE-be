from data.repositories.survey_features.question import Question
from data.repositories.survey_features.question_in_section import Question_in_section
from data.repositories.survey_features.question_option import Question_option
from services.survey_service.question_option import Question_option_service
from services.survey_service.question_option_section_mapping import (
    Question_option_section_mapping_service,
)
from services.survey_service.section import Section_service
from services.utils import Permission_check


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

    @classmethod
    def get_questions_in_survey(cls, sections_list_in_survey):
        return Question_in_section.get_questions_in_survey(sections_list_in_survey)

    @classmethod
    def get_question_detail_in_survey(cls, question_in_section_id, project_id, user_id):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        return Question_in_section.get_question_detail_in_survey(question_in_section_id)

    @classmethod
    def update_question_detail_in_survey(
        cls,
        user_id,
        project_id,
        section_id,
        question_in_section_id,
        question_type=None,
        is_required=None,
        order_in_section=None,
        weight=None,
        content=None,
    ):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        if order_in_section:
            cls.reorder_questions_in_section_when_change_position(
                section_id, question_in_section_id, order_in_section
            )
        if question_type:
            cls.change_question_type(question_in_section_id, question_type)

        return Question_in_section.update_question_detail_in_survey(
            question_in_section_id,
            question_type,
            is_required,
            order_in_section,
            weight,
            content,
        )

    @classmethod
    def reorder_questions_in_section_when_delete_question(
        cls, user_id, project_id, section_id, question_in_section_id
    ):
        # question_in_section_id is the id of the question that is being changed position or deleted
        # when the question is being deleted, the order of the remaining questions in the section should be updated
        # when the question is being changed position, the order of the questions in the section should be updated
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        # get the order of the question that is being changed position or deleted
        question_in_section = Question_in_section.get_question_in_section_by_id(
            question_in_section_id
        )
        order_of_question = question_in_section["orderInSection"]
        # get the list of questions in the section
        questions_in_section = Question_in_section.get_questions_in_section(section_id)
        # update the order of the questions in the section
        for question in questions_in_section:
            if question["orderInSection"] > order_of_question:
                Question_in_section.update_order_of_question_in_section(
                    question["id"], question["orderInSection"] - 1
                )

        return {"message": "Questions in section have been reordered"}

    @classmethod
    def reorder_questions_in_section_when_change_position(
        cls, section_id, question_in_section_id, new_order
    ):
        # get the order of the question that is being changed position or deleted
        question_in_section = Question_in_section.get_question_in_section_by_id(
            question_in_section_id
        )
        order_of_question = question_in_section["orderInSection"]
        # get the list of questions in the section
        questions_in_section = Question_in_section.get_questions_in_section(section_id)
        # update the order of the questions in the section
        for question in questions_in_section:
            if order_of_question < question["orderInSection"] < new_order:
                Question_in_section.update_order_of_question_in_section(
                    question["id"], question["orderInSection"] - 1
                )
            elif order_of_question > question["orderInSection"] >= new_order:
                Question_in_section.update_order_of_question_in_section(
                    question["id"], question["orderInSection"] + 1
                )

        # update the order of the question that is being changed position
        Question_in_section.update_order_of_question_in_section(
            question_in_section_id, new_order
        )
        return {"message": "Questions in section have been reordered"}

    @classmethod
    def delete_question_in_survey(
        cls, user_id, project_id, section_id, question_in_section_id
    ):
        is_user_has_access = Permission_check.check_user_has_access_survey(
            project_id, user_id
        )
        if not is_user_has_access:
            return {"message": "User has no access to the survey"}

        # delete the question in the section
        Question_in_section.delete_question_in_section(question_in_section_id)
        # delete the question options of the question if it has any
        Question_option.delete_question_option(question_in_section_id)
        # delete the question options section mapping of the question
        Question_option_section_mapping_service.delete_question_option_section_mapping(
            question_in_section_id
        )
        # reorder the questions in the section
        cls.reorder_questions_in_section_when_delete_question(
            user_id, project_id, section_id, question_in_section_id
        )
        return {"message": "Question has been deleted from the survey"}

    @classmethod
    def change_question_type(cls, question_in_section_id, new_question_type):
        # change question_type of the question
        # if the question is branching or multiple choice, then add question options to the question
        # if the question is already branching or multiple choice, then delete question options of the question
        # get the question in section
        question_in_section = Question_in_section.get_question_in_section_by_id(
            question_in_section_id
        )
        current_question_type = question_in_section["question_type"]
        # if the question is branching or multiple choice, then add question options to the question
        if new_question_type in ["branching", "multiple_choice"]:
            if current_question_type not in ["branching", "multiple_choice"]:
                question_options = Question_option.create_sample_question_option(
                    question_in_section, 1
                )
                # # for this branching question, create a sample mapping of question options to the next sections
                # question_options_section_mapping = Question_option_section_mapping_service.create_sample_question_option_section_mapping(
                #     question_options, Section_service.get_sections_in_survey()
                # )
        # if the question is already branching or multiple choice, then delete question options of the question
        else:
            if current_question_type in ["branching", "multiple_choice"]:
                Question_option.delete_question_option(question_in_section_id)
                # delete the question options section mapping of the question
                Question_option_section_mapping_service.delete_question_option_section_mapping(
                    question_in_section_id
                )
        return Question_in_section.change_question_type(
            question_in_section_id, new_question_type
        )

    @classmethod
    def add_new_question_to_section(
        cls,
        content,
        order_in_section,
        weight,
        is_required,
        question_type,
        section_id,
        question_options=None,
    ):
        # add question to the question table which is like a library of questions
        question = Question.create_question(content, question_type)
        # add question to the section
        question_in_section = Question_in_section.add_new_question_to_section(
            section_id, question, order_in_section, weight, is_required
        )
        # if the question_type is branching or multiple choice, then add question options to the question
        if question_options:
            question_options = Question_option_service.create_question_options(
                question_in_section, question_options
            )
            # # for this branching question, create a sample mapping of question options to the next sections
            # question_options_section_mapping = Question_option_section_mapping_service.create_sample_question_option_section_mapping(
            #     question_options, Section_service.get_sections_in_survey()
            # )

        return question_in_section
