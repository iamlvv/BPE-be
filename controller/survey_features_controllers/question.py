import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.question_in_section import Question_in_section_service


@bpsky.route("/api/v1/survey/question/<question_in_section_id>", methods=["GET"])
def get_question_detail_in_survey(question_in_section_id):
    user_id = get_id_from_token(get_token(request))
    project_id = request.args.get("projectId", None)
    data = Question_in_section_service.get_question_detail_in_survey(
        question_in_section_id, project_id, user_id
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )
