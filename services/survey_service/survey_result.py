from data.repositories.survey_features.survey_result import Survey_result


class Survey_result_service:
    @classmethod
    def calculate_scores(cls, survey_id, current_number_of_responses):
        # get all answers for response_id
        # get all questions for survey_id
        # calculate scores
        # update response with scores
        ces_score = cls.calculate_ces_score(survey_id, current_number_of_responses)
        nps_score = cls.calculate_nps_score(survey_id, current_number_of_responses)
        csat_score = cls.calculate_csat_score(survey_id, current_number_of_responses)
        # get weight of each score in survey
        # calculate final score
        # update survey with final score
        weights_of_scores = Survey_result.get_weights_of_scores(survey_id)
        ces_weight = weights_of_scores.ces_weight
        nps_weight = weights_of_scores.nps_weight
        csat_weight = weights_of_scores.csat_weight
        final_score = (
            ces_score["ces_score"] * ces_weight
            + nps_score["nps_score"] * nps_weight
            + csat_score["csat_score"] * csat_weight
        ) / (ces_weight + nps_weight + csat_weight)
        return {
            "ces_score": ces_score["ces_score"],
            "nps_score": nps_score["nps_score"],
            "csat_score": csat_score["csat_score"],
            "final_score": round(final_score, 3),
        }

    @classmethod
    def calculate_ces_or_csat_score(
        cls, survey_id, current_number_of_responses, question_type
    ):
        # get all ces answers for survey_id
        # get weight of ces questions
        # calculate ces score with formula: sum of ces answer of each question * weight of each question / total
        # number of responses
        # update survey with ces score
        list_of_weight_and_answers_of_questions_in_survey = (
            cls.get_list_of_weight_and_answers_of_questions_in_survey(survey_id, "ces")
        )
        total_number_of_responses = current_number_of_responses  # get from response
        sum_of_weight = 0  # sum of weight of all questions
        result = 0
        dict_positive_answers_for_each_question = (
            {}
        )  # table of number of answers has value 5, 6, 7, key is question_id, value is number of answers
        dict_weight = (
            {}
        )  # table of weight of each question, key is question_id, value is weight

        for item in list_of_weight_and_answers_of_questions_in_survey:
            if item["value"] in ["5", "6", "7"]:
                # get number of answers has value 5, 6, 7
                dict_positive_answers_for_each_question[item["question_id"]] = (
                    dict_positive_answers_for_each_question.get(item["question_id"], 0)
                    + 1
                )
                dict_weight[item["question_id"]] = item["weight"]
        for index in dict_weight:
            sum_of_weight += dict_weight[index]
        for index in dict_positive_answers_for_each_question:
            result += (
                dict_positive_answers_for_each_question[index]
                * dict_weight[index]
                / (total_number_of_responses * sum_of_weight)
            )

        # return round(result, 3)
        return {
            "ces_score" if question_type == "ces" else "csat_score": round(result, 3),
            "list_of_weight_and_answers_of_questions_in_survey": list_of_weight_and_answers_of_questions_in_survey,
            "total_number_of_responses": total_number_of_responses,
            "sum_of_weight": sum_of_weight,
            "dict_positive_answers_for_each_question": dict_positive_answers_for_each_question,
            "dict_weight": dict_weight,
        }

    @classmethod
    def calculate_ces_score(cls, survey_id, current_number_of_responses):
        return cls.calculate_ces_or_csat_score(
            survey_id, current_number_of_responses, "ces"
        )

    @classmethod
    def calculate_nps_score(cls, survey_id, current_number_of_responses):
        list_of_weight_and_answers_of_questions_in_survey = (
            cls.get_list_of_weight_and_answers_of_questions_in_survey(survey_id, "nps")
        )
        total_number_of_responses = current_number_of_responses
        sum_of_weight = 0
        result = 0
        dict_weight = {}
        dict_promoters_for_each_question = (
            {}
        )  # table of number of answers has value 9, 10, key is question_id, value is number of answers
        dict_passives_for_each_question = (
            {}
        )  # table of number of answers has value 7, 8, key is question_id, value is number of answers
        dict_detractors_for_each_question = (
            {}
        )  # table of number of answers has value 0, 1, 2, 3, 4, 5, 6, key is question_id, value is number of answers
        for item in list_of_weight_and_answers_of_questions_in_survey:
            if item["value"] in ["9", "10"]:
                dict_promoters_for_each_question[item["question_id"]] = (
                    dict_promoters_for_each_question.get(item["question_id"], 0) + 1
                )
                dict_weight[item["question_id"]] = item["weight"]
            elif item["value"] in ["7", "8"]:
                dict_passives_for_each_question[item["question_id"]] = (
                    dict_passives_for_each_question.get(item["question_id"], 0) + 1
                )
                dict_weight[item["question_id"]] = item["weight"]
            elif item["value"] in ["0", "1", "2", "3", "4", "5", "6"]:
                dict_detractors_for_each_question[item["question_id"]] = (
                    dict_detractors_for_each_question.get(item["question_id"], 0) + 1
                )
                dict_weight[item["question_id"]] = item["weight"]
        for index in dict_weight:
            sum_of_weight += dict_weight[index]
        for index in dict_promoters_for_each_question:
            result += (
                dict_promoters_for_each_question[index]
                * dict_weight[index]
                / (total_number_of_responses * sum_of_weight)
            )
        for index in dict_detractors_for_each_question:
            result -= (
                dict_detractors_for_each_question[index]
                * dict_weight[index]
                / (total_number_of_responses * sum_of_weight)
            )
        return {
            "nps_score": round(result, 3),
            "list_of_weight_and_answers_of_questions_in_survey": list_of_weight_and_answers_of_questions_in_survey,
            "total_number_of_responses": total_number_of_responses,
            "sum_of_weight": sum_of_weight,
            "dict_promoters_for_each_question": dict_promoters_for_each_question,
            "dict_passives_for_each_question": dict_passives_for_each_question,
            "dict_detractors_for_each_question": dict_detractors_for_each_question,
            "dict_weight": dict_weight,
        }

    @classmethod
    def calculate_csat_score(cls, survey_id, current_number_of_responses):
        return cls.calculate_ces_or_csat_score(
            survey_id, current_number_of_responses, "csat"
        )

    @classmethod
    def get_list_of_weight_and_answers_of_questions_in_survey(
        cls, survey_id, question_type
    ):
        list_of_weight_and_answers_of_questions_in_survey = (
            Survey_result.get_list_of_weight_and_answers_of_questions_in_survey(
                survey_id, question_type
            )
        )
        return [
            {
                "question_id": item.id,
                "value": item.value,
                "weight": item.weight,
            }
            for item in list_of_weight_and_answers_of_questions_in_survey
        ]
