import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.question import Question_service
from services.survey_service.question_in_section import Question_in_section_service


@bpsky.route("/api/v1/survey/question", methods=["GET"])
def get_question_detail_in_survey():
    user_id = get_id_from_token(get_token(request))
    project_id = request.args.get("projectId", None)
    question_in_section_id = request.args.get("questionInSectionId", None)
    data = Question_in_section_service.get_question_detail_in_survey(
        question_in_section_id, project_id, user_id
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/question", methods=["PUT"])
def update_question_detail_in_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    content = body["content"] if "content" in body else None
    question_type = body["questionType"] if "questionType" in body else None
    is_required = body["isRequired"] if "isRequired" in body else None
    order_in_section = body["orderInSection"] if "orderInSection" in body else None
    project_id = body["projectId"]
    weight = body["weight"] if "weight" in body else None
    question_in_section_id = body["questionInSectionId"]
    section_id = body["sectionId"]
    data = Question_in_section_service.update_question_detail_in_survey(
        user_id,
        project_id,
        section_id,
        question_in_section_id,
        question_type,
        is_required,
        order_in_section,
        weight,
        content,
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/init", methods=["POST"])
def initialize_sample_questions():
    user_id = get_id_from_token(get_token(request))
    data = Question_service.initialize_sample_questions()
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/question", methods=["DELETE"])
def delete_question_in_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    project_id = body["projectId"]
    question_in_section_id = body["questionInSectionId"]
    section_id = body["sectionId"]
    data = Question_in_section_service.delete_question_in_survey(
        user_id, project_id, section_id, question_in_section_id
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )
