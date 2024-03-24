from datetime import datetime

from data.models.process_portfolio_feature_models.process_portfolio_model import (
    Process_portfolio_model,
)
from database.db import DatabaseConnector


class Process_portfolio:
    @classmethod
    def add_process_portfolio(cls, workspace_id):
        session = DatabaseConnector.get_session()
        try:
            process_portfolio = Process_portfolio_model(
                workspace_id=workspace_id, is_deleted=False, created_at=datetime.now()
            )
            session.add(process_portfolio)
            session.commit()
            return process_portfolio
        except Exception as e:
            session.rollback()
            raise Exception(e)
        finally:
            session.close()

    @classmethod
    def check_if_process_portfolio_exists(cls, workspace_id):
        session = DatabaseConnector.get_session()
        try:
            process_portfolio = (
                session.query(Process_portfolio_model)
                .filter(Process_portfolio_model.workspace_id == workspace_id)
                .first()
            )
            session.commit()
            return process_portfolio
        except Exception as e:
            session.rollback()
            raise Exception(e)
        finally:
            session.close()
