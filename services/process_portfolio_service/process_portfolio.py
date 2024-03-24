from data.repositories.process_portfolio_features.process_portfolio import (
    Process_portfolio,
)
from services.process_portfolio_service.feasibility import Feasibility_service
from services.process_portfolio_service.health import Health_service
from services.process_portfolio_service.strategic_importance import (
    Strategic_importance_service,
)
from services.utils import Permission_check


class Process_portfolio_service:
    @classmethod
    def create_process_portfolio(
        cls, workspace_id, user_id, active_process_version_list
    ):
        try:
            workspace_owner = Permission_check.check_if_user_is_workspace_owner(
                workspace_id, user_id
            )
            if not workspace_owner:
                raise Exception("permission denied")

            # check if item in active_process_version_list exists in table Health, Strategic Importance, Feasibility
            cls.check_if_active_process_versions_have_health_strategic_importance_feasibility(
                active_process_version_list
            )
            # check if process portfolio exists in table Process_portfolio
            process_portfolio = cls.check_if_process_portfolio_exists(workspace_id)
            if process_portfolio:
                return {
                    "id": process_portfolio.id,
                    "createdAt": process_portfolio.created_at,
                    "isDeleted": process_portfolio.is_deleted,
                    "workspaceId": process_portfolio.workspace_id,
                }
            process_portfolio = Process_portfolio.add_process_portfolio(workspace_id)
            return {
                "id": process_portfolio.id,
                "createdAt": process_portfolio.created_at,
                "isDeleted": process_portfolio.is_deleted,
                "workspaceId": process_portfolio.workspace_id,
            }
        except Exception as e:
            raise Exception(e)

    @classmethod
    def check_if_process_portfolio_exists(cls, workspace_id):
        return Process_portfolio.check_if_process_portfolio_exists(workspace_id)

    @classmethod
    def check_if_active_process_versions_have_health_strategic_importance_feasibility(
        cls, active_process_version_list
    ):
        try:
            for active_process_version in active_process_version_list:
                Health_service.check_if_process_version_exists_in_health(
                    active_process_version
                )
                Feasibility_service.check_if_process_version_exists_in_feasibility(
                    active_process_version
                )
                Strategic_importance_service.check_if_process_version_exists_in_strategic_importance(
                    active_process_version
                )
        except Exception as e:
            raise Exception(e)
