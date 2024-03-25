from datetime import timezone

import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.survey import Survey_service


@bpsky.route("/api/v1/survey", methods=["GET"])
def get_survey_detail():
    user_id = get_id_from_token(get_token(request))
    process_version_version = request.args.get("processVersionVersion", None)
    project_id = request.args.get("projectId", None)
    data = Survey_service.get_survey_detail(
        process_version_version, project_id, user_id
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey", methods=["POST"])
def create_new_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    # survey_name = body["name"]
    # survey_description = body["description"]
    process_version_version = body["processVersionVersion"]
    project_id = body["projectId"]

    # check if the survey has been created for the process version before, because a process version
    # only have 1 existing survey
    survey_id_exists = Survey_service.check_if_survey_exists(process_version_version)
    if survey_id_exists:
        data = Survey_service.get_survey_content(
            user_id, project_id, process_version_version
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    data = Survey_service.create_new_survey(
        project_id, user_id, process_version_version
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/edit", methods=["GET"])
def get_survey_content():
    user_id = get_id_from_token(get_token(request))
    process_version_version = request.args.get("processVersionVersion", None)
    project_id = request.args.get("projectId", None)
    data = Survey_service.get_survey_content(
        user_id, project_id, process_version_version
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey", methods=["DELETE"])
def delete_survey():
    user_id = get_id_from_token(get_token(request))
    survey_id = request.args.get("surveyId", None)
    project_id = request.args.get("projectId", None)
    data = Survey_service.delete_survey(user_id, project_id, survey_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/general_configuration", methods=["GET"])
def get_survey_general_config():
    user_id = get_id_from_token(get_token(request))
    survey_id = request.args.get("surveyId")
    project_id = request.args.get("projectId")
    data = Survey_service.get_survey_general_config(survey_id, user_id, project_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/general_configuration", methods=["PUT"])
def config_survey_general():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    project_id = body["projectId"]
    survey_id = body["surveyId"]
    survey_name = body["name"] if "name" in body else None
    survey_description = body["description"] if "description" in body else None
    nps_weight = body["npsWeight"] if "npsWeight" in body else None
    ces_weight = body["cesWeight"] if "cesWeight" in body else None
    csat_weight = body["csatWeight"] if "csatWeight" in body else None
    data = Survey_service.config_survey_general(
        survey_id,
        user_id,
        project_id,
        survey_name,
        survey_description,
        nps_weight,
        ces_weight,
        csat_weight,
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/response_configuration", methods=["GET"])
def get_survey_response_config():
    user_id = get_id_from_token(get_token(request))
    survey_id = request.args.get("surveyId")
    project_id = request.args.get("projectId")
    data = Survey_service.get_survey_response_config(survey_id, user_id, project_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/response_configuration", methods=["PUT"])
def config_survey_response():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    project_id = body["projectId"]
    survey_id = body["surveyId"]
    incomplete_survey_action = (
        body["incompleteSurveyAction"] if "incompleteSurveyAction" in body else None
    )
    allow_duplicate_respondent = (
        body["allowDuplicateRespondent"] if "allowDuplicateRespondent" in body else None
    )
    send_result_to_respondent = (
        body["sendResultToRespondent"] if "sendResultToRespondent" in body else None
    )
    start_date = body["startDate"] if "startDate" in body else None
    end_date = body["endDate"] if "endDate" in body else None

    # convert to datetime object, including hours, minutes, and seconds
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

    data = Survey_service.config_survey_response(
        survey_id,
        user_id,
        project_id,
        incomplete_survey_action,
        allow_duplicate_respondent,
        send_result_to_respondent,
        start_date,
        end_date,
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/publish", methods=["POST"])
def publish_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    process_version_version = body["processVersionVersion"]
    project_id = body["projectId"]
    start_date = body["startDate"] if "startDate" in body else None
    end_date = body["endDate"] if "endDate" in body else None
    email = body["email"] if "email" in body else None
    survey_url = body["surveyUrl"]
    if start_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    if end_date is not None:
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

    data = Survey_service.publish_survey(
        process_version_version,
        project_id,
        user_id,
        survey_url,
        email,
        start_date,
        end_date,
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )
