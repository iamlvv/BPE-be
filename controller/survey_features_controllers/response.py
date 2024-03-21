import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.response import Response_service
from services.survey_service.survey import Survey_service


@bpsky.route("/api/v1/survey/section", methods=["GET"])
def get_survey_questions_by_section_id():
    section_id = request.args.get("sectionId", None)
    data = Survey_service.get_survey_questions_by_section_id(section_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/section/all", methods=["GET"])
def get_survey_sections():
    process_version_version = request.args.get("processVersionVersion", None)
    data = Survey_service.get_sections_in_survey(process_version_version)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/submission", methods=["POST"])
def submit_survey_form():
    body = load_request_body(request)
    process_version_version = body["processVersionVersion"]
    answers = body["answers"]
    email = body["email"]
    full_name = body["fullName"]
    data = Response_service.submit_survey_form(
        answers, email, full_name, process_version_version
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/response", methods=["GET"])
def get_survey_response():
    response_id = request.args.get("responseId", None)
    data = Response_service.get_survey_response(response_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/publish/close", methods=["POST"])
def close_publish_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    project_id = body["projectId"]
    process_version_version = body["processVersionVersion"]
    data = Survey_service.close_publish_survey(
        user_id, project_id, process_version_version
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )
