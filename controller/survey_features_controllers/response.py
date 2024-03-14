import jsonpickle

from bpsky import bpsky
from controller.utils import *
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
