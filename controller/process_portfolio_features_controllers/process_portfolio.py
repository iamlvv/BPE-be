import jsonpickle

from bpsky import bpsky
from controller.utils import *


@bpsky.route("/api/v1/workspace/portfolio/projects", methods=["GET"])
def get_all_projects_in_workspace():
    user_id = get_id_from_token(get_token(request))
    workspace_id = request.args.get("workspaceId")
    data = ProjectService.get_all_projects_in_workspace(workspace_id, user_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/workspace/portfolio/processversion", methods=["GET"])
def get_all_active_process_versions_in_workspace():
    try:
        user_id = get_id_from_token(get_token(request))
        workspace_id = request.args.get("workspaceId")
        project_id = request.args.get("projectId")
        data = ProcessService.get_all_active_process_versions_in_workspace(
            workspace_id, project_id, user_id
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/processversion/active", methods=["POST"])
def active_process_version():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        workspace_id = body["workspaceId"]
        process_version_version = body["processVersionVersion"]
        data = ProcessVersionService.active_process_version(
            user_id, workspace_id, process_version_version
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)
