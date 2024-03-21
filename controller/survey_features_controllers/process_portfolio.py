import jsonpickle

from bpsky import bpsky
from controller.utils import *


@bpsky.route("/api/v1/workspace/portfolio/projects", methods=["GET"])
def get_all_projects_in_workspace():
    user_id = get_id_from_token(get_token(request))
    workspace_id = request.args.get("workspaceId")
    data = ProjectService.getAllProjectsInWorkspace(workspace_id, user_id)
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/workspace/portfolio/projects/<int:project_id>", methods=["GET"])
def get_all_active_process_versions_in_workspace(project_id):
    try:
        user_id = get_id_from_token(get_token(request))
        workspace_id = request.args.get("workspaceId")
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
