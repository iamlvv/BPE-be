from .utils import *


@bpsky.route("/api/v1/result/all", methods=["POST"])
def evaluated_result_get_result_by_bpmn_file():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        data = EvaluatedResultUsercase.get_all_result_by_bpmn_file(
            user_id, project_id, xml_file_link)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/result/<int:project_id>/save", methods=["POST"])
def evaluated_result_save(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["xmlFileLink", "name", "result"]:
            if i not in body:
                raise Exception(i + " required")
        xml_file_link = body['xmlFileLink']
        name = body['name']
        result = body['result']
        description = body['description'] if 'description' in body else ""
        EvaluatedResultUsercase.save(user_id, xml_file_link, project_id, name, result,
                                     description)
        return "Create successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/result", methods=["POST"])
def evaluated_result_get():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink", "name"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        name = body['name']
        data = EvaluatedResultUsercase.get_result(
            user_id, project_id,  xml_file_link, name)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/result/delete", methods=["DELETE"])
def evaluated_result_delete():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink", "name"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        name = body['name']
        EvaluatedResultUsercase.delete(
            user_id,  xml_file_link, project_id, name)
        return "Delete successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )
