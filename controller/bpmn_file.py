from .utils import *


@bpsky.route("/api/v1/bpmnfile/<int:project_id>/<string:version>/save", methods=["PUT"])
def bpmn_file_save(project_id, version):
    try:
        user_id = get_id_from_token(get_token(request))
        if "file" not in request.files:
            raise Exception("file required")
        if "xmlFileLink" not in request.form:
            raise Exception("xmlFileLink required")
        file = request.files['file']
        xml_file_link = request.form['xmlFileLink']
        BPMNFileUsecase.save(xml_file_link, file,
                             user_id, project_id, version)
        return "Save successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/<int:project_id>/create", methods=["POST"])
def bpmn_file_create_new_version(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        if "file" not in request.files:
            raise Exception("file required")
        file = request.files['file']
        BPMNFileUsecase.create_new_version(user_id, file, project_id)
        return "Create successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/delete_oldest/<int:project_id>", methods=["DELETE"])
def bpmn_file_delete_oldest_version(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        BPMNFileUsecase.delete_oldest_version(user_id, project_id)
        return "Delete successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/<int:project_id>/<string:version>/delete", methods=["DELETE"])
def bpmn_file_delete_version(project_id, version):
    try:
        user_id = get_id_from_token(get_token(request))
        BPMNFileUsecase.delete_version(user_id, project_id, version)
        return "Delete successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/<int:project_id>", methods=["GET"])
def bpmn_file_get_by_project(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        versions = BPMNFileUsecase.get_by_project(user_id, project_id)
        return versions
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/<int:project_id>/<string:version>", methods=["GET"])
def bpmn_file_get_by_version(project_id, version):
    try:
        user_id = get_id_from_token(get_token(request))
        xml_file_link = BPMNFileUsecase.get_by_version(
            user_id, project_id, version)
        return xml_file_link
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/<int:project_id>/<string:version>/text", methods=["GET"])
def bpmn_file_get_content_by_version(project_id, version):
    try:
        user_id = get_id_from_token(get_token(request))
        content = BPMNFileUsecase.get_content_by_version(
            user_id, project_id, version)
        return bpsky.response_class(
            response=content,
            content_type="xml",
            status=200
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/comment/add", methods=["POST"])
def bpmn_file_comment():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink", "content"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        content = body['content']
        data = BPMNFileUsecase.comment(
            user_id, project_id, xml_file_link, content)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            content_type="json",
            status=200
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/comment/edit", methods=["PUT"])
def bpmn_file_edit_comment():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink", "id", "content"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        id = body['id']
        content = body['content']
        BPMNFileUsecase.edit_comment(
            user_id, project_id, xml_file_link, id, content)
        return "Edit successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/comment/delete", methods=["DELETE"])
def bpmn_file_delete_comment():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink", "id"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        id = body['id']
        BPMNFileUsecase.delete_comment(
            user_id, project_id, xml_file_link, id)
        return "Delete successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/comment", methods=["POST"])
def bpmn_file_get_comment_by_bpmn_file():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        data = BPMNFileUsecase.get_comment_by_bpmn_file(
            user_id, project_id, xml_file_link)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            content_type="json",
            status=200
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/comment/user", methods=["POST"])
def bpmn_file_get_comment_by_user():
    try:
        user_id = get_id_from_token(get_token(request))
        data = BPMNFileUsecase.get_comment_by_user(user_id)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            content_type="json",
            status=200
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/image", methods=["POST"])
def bpmn_file_get_image_by_bpmn_file():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        for i in ["projectID", "xmlFileLink"]:
            if i not in body:
                raise Exception(i + " required")
        project_id = body['projectID']
        xml_file_link = body['xmlFileLink']
        data = ImageUsecase.get_image_by_bpmn_file(
            user_id, project_id, xml_file_link)
        return bpsky.response_class(
            response=json.dumps(data, default=json_serial),
            content_type="json",
            status=200
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/api/v1/bpmnfile/image/add", methods=["POST"])
def bpmn_file_add_image():
    try:
        user_id = get_id_from_token(get_token(request))
        if "file" not in request.files:
            raise Exception("file required")
        for i in ["projectID", "xmlFileLink"]:
            if i not in request.form:
                raise Exception(i + " required")
        file = request.files['file']
        project_id = request.form['projectID']
        xml_file_link = request.form['xmlFileLink']
        ImageUsecase.insert_image(
            user_id, project_id, xml_file_link, file)
        return "Create successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )
