import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.survey import Survey_service


@bpsky.route("/api/v1/survey/<survey_id>", methods=["GET"])
def get_survey_detail(survey_id):
    user_id = get_id_from_token(get_token(request))
    project_id = request.args.get("projectId", None)
    data = Survey_service.get_survey_detail(survey_id, project_id, user_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey", methods=["POST"])
def create_new_survey():
    user_id = get_id_from_token(get_token(request))
    body = load_request_body(request)
    survey_name = body["name"]
    survey_description = body["description"]
    process_version_version = body["processVersionVersion"]
    project_id = body["projectId"]
    data = Survey_service.create_new_survey(
        project_id, user_id, survey_name, survey_description, process_version_version
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/survey/edit", methods=["GET"])
def get_survey_content():
    user_id = get_id_from_token(get_token(request))
    survey_id = request.args.get("surveyId", None)
    project_id = request.args.get("projectId", None)
    data = Survey_service.get_survey_content(user_id, project_id, survey_id)
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


@bpsky.route("/api/v1/survey/general", methods=["PUT"])
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
