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
    ):
        session = DatabaseConnector.get_session()
        try:
            process_version_health = (
                session.query(Health_model)
                .filter(Health_model.process_version_version == process_version_version)
                .first()
            )
            if targeted_cycle_time is not None:
                process_version_health.targeted_cycle_time = targeted_cycle_time
            if worst_cycle_time is not None:
                process_version_health.worst_cycle_time = worst_cycle_time
            if current_cycle_time is not None:
                process_version_health.current_cycle_time = current_cycle_time
            if targeted_cost is not None:
                process_version_health.targeted_cost = targeted_cost
            if worst_cost is not None:
                process_version_health.worst_cost = worst_cost
            if current_cost is not None:
                process_version_health.current_cost = current_cost
            if targeted_quality is not None:
                process_version_health.targeted_quality = targeted_quality
            if worst_quality is not None:
                process_version_health.worst_quality = worst_quality
            if current_quality is not None:
                process_version_health.current_quality = current_quality
            if targeted_flexibility is not None:
                process_version_health.targeted_flexibility = targeted_flexibility
            if worst_flexibility is not None:
                process_version_health.worst_flexibility = worst_flexibility
            if current_flexibility is not None:
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
    ):
        session = DatabaseConnector.get_session()
        try:
            health = Health_model(
                process_version_version=process_version_version,
                targeted_cycle_time=targeted_cycle_time,
                worst_cycle_time=worst_cycle_time,
                current_cycle_time=current_cycle_time,
                targeted_cost=targeted_cost,
                worst_cost=worst_cost,
                current_cost=current_cost,
                targeted_quality=targeted_quality,
                worst_quality=worst_quality,
                current_quality=current_quality,
                targeted_flexibility=targeted_flexibility,
                worst_flexibility=worst_flexibility,
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
