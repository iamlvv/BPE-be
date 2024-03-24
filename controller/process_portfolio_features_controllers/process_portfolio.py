import jsonpickle

from bpsky import bpsky
from controller.utils import *
from services.process_portfolio_service.feasibility import Feasibility_service
from services.process_portfolio_service.health import Health_service
from services.process_portfolio_service.strategic_importance import (
    Strategic_importance_service,
)


@bpsky.route("/api/v1/workspace/portfolio/projects", methods=["GET"])
def get_all_projects_in_workspace():
    user_id = get_id_from_token(get_token(request))
    workspace_id = request.args.get("workspaceId")
    page = request.args.get("page", 0)
    limit = request.args.get("limit", 10)
    data = ProjectService.get_all_projects_in_workspace(
        workspace_id, user_id, page, limit
    )
    return bpsky.response_class(
        response=jsonpickle.encode(data, unpicklable=False),
        status=200,
        mimetype="application/json",
    )


@bpsky.route("/api/v1/workspace/portfolio/processes", methods=["GET"])
def get_all_processes_in_project():
    try:
        user_id = get_id_from_token(get_token(request))
        workspace_id = request.args.get("workspaceId")
        project_id = request.args.get("projectId")
        data = ProcessService.get_all_processes_in_project(
            workspace_id, project_id, user_id
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/processversion", methods=["GET"])
def get_all_process_versions_in_process():
    try:
        user_id = get_id_from_token(get_token(request))
        workspace_id = request.args.get("workspaceId")
        process_id = request.args.get("processId")
        data = ProcessVersionService.get_all_process_versions_in_process(
            workspace_id, process_id, user_id
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/processversion/activation", methods=["POST"])
def activate_process_version():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        workspace_id = body["workspaceId"]
        process_version_version = body["processVersionVersion"]
        data = ProcessVersionService.activate_process_version(
            user_id, workspace_id, process_version_version
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/health", methods=["GET"])
def get_health_of_active_process_versions_in_workspace():
    try:
        user_id = get_id_from_token(get_token(request))

        workspace_id = request.args.get("workspaceId")
        data = Health_service.get_health_of_active_process_versions_in_workspace(
            workspace_id, user_id
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/health", methods=["POST"])
def edit_health_of_active_process_version():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        workspace_id = body["workspaceId"]
        process_version_version = body["processVersionVersion"]
        targeted_cycle_time = (
            body["targetedCycleTime"] if "targetedCycleTime" in body else None
        )
        worst_cycle_time = body["worstCycleTime"] if "worstCycleTime" in body else None
        current_cycle_time = (
            body["currentCycleTime"] if "currentCycleTime" in body else None
        )

        targeted_cost = body["targetedCost"] if "targetedCost" in body else None
        worst_cost = body["worstCost"] if "worstCost" in body else None
        current_cost = body["currentCost"] if "currentCost" in body else None

        targeted_quality = (
            body["targetedQuality"] if "targetedQuality" in body else None
        )
        worst_quality = body["worstQuality"] if "worstQuality" in body else None
        current_quality = body["currentQuality"] if "currentQuality" in body else None

        targeted_flexibility = (
            body["targetedFlexibility"] if "targetedFlexibility" in body else None
        )
        worst_flexibility = (
            body["worstFlexibility"] if "worstFlexibility" in body else None
        )
        current_flexibility = (
            body["currentFlexibility"] if "currentFlexibility" in body else None
        )

        data = Health_service.edit_health_of_active_process_versions(
            workspace_id,
            process_version_version,
            user_id,
            targeted_cycle_time,
            worst_cycle_time,
            current_cycle_time,
            targeted_cost,
            worst_cost,
            current_cost,
            targeted_quality,
            worst_quality,
            current_quality,
            targeted_flexibility,
            worst_flexibility,
            current_flexibility,
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/feasibility", methods=["POST"])
def edit_feasibility_of_active_process_version():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        workspace_id = body["workspaceId"]
        process_version_version = body["processVersionVersion"]
        total_score = body["totalScore"]
        data = Feasibility_service.edit_feasibility_of_active_process_versions(
            workspace_id, process_version_version, user_id, total_score
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/workspace/portfolio/strategic_importance", methods=["POST"])
def edit_strategic_importance_of_active_process_version():
    try:
        user_id = get_id_from_token(get_token(request))
        body = load_request_body(request)
        workspace_id = body["workspaceId"]
        process_version_version = body["processVersionVersion"]
        total_score = body["totalScore"]
        data = Strategic_importance_service.edit_strategic_importance_of_active_process_version(
            workspace_id, process_version_version, user_id, total_score
        )
        return bpsky.response_class(
            response=jsonpickle.encode(data, unpicklable=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)