Class Question_option_section_mapping_service:
    @classmethod
    def create_sample_question_option_section_mapping(cls, question_options_list, sections_list_in_survey):
        # only create question option section mapping for multiple choice questions and branching questions
        # they are the first 2 questions in the survey
        question_option_section_mapping = []
        for i in range(0, 2):
            question = sections_list_in_survey[i]
            if question["type"] in ["multiple_choice", "branching"]:
                # create question option section mapping
                question_option_section_mapping.append(
                    Question_option_section_mapping.create_sample_question_option_section_mapping(question, i)
                )
                # add question option section mapping to the question
        return question_option_section_mapping