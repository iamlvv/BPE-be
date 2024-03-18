import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.survey_service.survey_result import Survey_result_service


@bpsky.route("/api/v1/survey/result", methods=["GET"])
def get_survey_result():
    survey_id = request.args.get("surveyId", None)
    data = Survey_result_service.get_survey_result(survey_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )
