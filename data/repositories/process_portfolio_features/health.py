from data.models.process_portfolio_feature_models.process_portfolio_model import (
    Health_model,
)
from database.db import DatabaseConnector


class Health:
    @classmethod
    def check_if_process_version_exists_in_health(cls, process_version_version):
        session = DatabaseConnector.get_session()
        try:
            process_version = (
                session.query(Health_model)
                .filter(Health_model.process_version_version == process_version_version)
                .first()
            )
            session.commit()
            return process_version
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def update_health_of_active_process_version(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        session = DatabaseConnector.get_session()
        try:
            process_version_health = (
                session.query(Health_model)
                .filter(Health_model.process_version_version == process_version_version)
                .first()
            )

            process_version_health.current_cycle_time = current_cycle_time

            process_version_health.current_cost = current_cost

            process_version_health.current_quality = current_quality

            process_version_health.current_flexibility = current_flexibility

            session.commit()
            return process_version_health
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def add_health_of_active_process_version(
        cls,
        process_version_version,
        current_cycle_time,
        current_cost,
        current_quality,
        current_flexibility,
    ):
        session = DatabaseConnector.get_session()
        try:
            health = Health_model(
                process_version_version=process_version_version,
                current_cycle_time=current_cycle_time,
                current_cost=current_cost,
                current_quality=current_quality,
                current_flexibility=current_flexibility,
            )
            session.add(health)
            session.commit()
            return health
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def get_health_of_active_process_version(cls, process_version_version):
        session = DatabaseConnector.get_session()
        try:
            health = (
                session.query(Health_model)
                .filter(Health_model.process_version_version == process_version_version)
                .first()
            )
            session.commit()
            return health
        except Exception as e:
            session.rollback()
            raise Exception(e)
