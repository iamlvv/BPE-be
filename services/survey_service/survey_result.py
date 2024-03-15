from data.repositories.survey_features.survey_result import Survey_result


class Survey_result_service:
    @classmethod
    def calculate_scores(cls, survey_id, current_number_of_responses):
        # get all answers for response_id
        # get all questions for survey_id
        # calculate scores
        # update response with scores
        return cls.calculate_ces_score(survey_id, current_number_of_responses)

    @classmethod
    def calculate_ces_score(cls, survey_id, current_number_of_responses):
        # get all ces answers for survey_id
        # get weight of ces questions
        # calculate ces score with formula: sum of ces answer of each question * weight of each question / total
        # number of responses
        # update survey with ces score
        list_weight_questions_and_answers = cls.get_list_of_weight_of_ces_questions(
            survey_id
        )
        total_number_of_responses = current_number_of_responses
        sum_of_weighted_answers = 0
        sum_of_weight = 0
        number_of_positive_result = 0
        sum = 0
        result = {}
        dict_weight = {}

        for item in list_weight_questions_and_answers:
            if item["value"] in ["5", "6", "7"]:
                # get number of answers has value 5, 6, 7
                result[item["question_id"]] = result.get(item["question_id"], 0) + 1
                dict_weight[item["question_id"]] = item["weight"]
        for index in dict_weight:
            sum_of_weight += dict_weight[index]
        for index in result:
            print(
                result[index],
                dict_weight[index],
                total_number_of_responses,
                sum_of_weight,
            )
            sum += (
                result[index]
                * dict_weight[index]
                / (total_number_of_responses * sum_of_weight)
            )

        return round(sum, 3)

    @classmethod
    def calculate_nps_score(cls, survey_id, current_number_of_responses):
        pass

    @classmethod
    def calculate_csat_score(cls, survey_id, current_number_of_responses):
        pass

    @classmethod
    def get_list_of_weight_of_ces_questions(cls, survey_id):
        return Survey_result.get_list_of_weight_of_ces_questions(survey_id)
