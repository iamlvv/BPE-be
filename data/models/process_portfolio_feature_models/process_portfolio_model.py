import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.meta_data import Base
from data.models.survey_feature_models.survey_model import (
    Survey_model,
    Process_version_model,
    Project_model,
)
from database.db import DatabaseConnector


class Health_model(Base):
    __tablename__ = "health"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_score: Mapped[float] = mapped_column(nullable=True)

    targeted_cycle_time: Mapped[float] = mapped_column(nullable=True)
    current_cycle_time: Mapped[float] = mapped_column(nullable=True)
    worst_cycle_time: Mapped[float] = mapped_column(nullable=True)

    targeted_cost: Mapped[float] = mapped_column(nullable=True)
    current_cost: Mapped[float] = mapped_column(nullable=True)
    worst_cost: Mapped[float] = mapped_column(nullable=True)

    targeted_quality: Mapped[float] = mapped_column(nullable=True)
    current_quality: Mapped[float] = mapped_column(nullable=True)
    worst_quality: Mapped[float] = mapped_column(nullable=True)

    targeted_flexibility: Mapped[float] = mapped_column(nullable=True)
    current_flexibility: Mapped[float] = mapped_column(nullable=True)
    worst_flexibility: Mapped[float] = mapped_column(nullable=True)

    # foreign key
    process_portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("process_portfolio.id"), nullable=False
    )
    process_version_version: Mapped[str] = mapped_column(
        ForeignKey("process_version.version"), nullable=False
    )

    # relationship
    process_version = relationship("Process_version_model", backref="health")
    process_portfolio = relationship("Process_portfolio_model", backref="health")


class Feasibility_model(Base):
    __tablename__ = "feasibility"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    total_score: Mapped[float] = mapped_column(nullable=True)

    # foreign key
    process_portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("process_portfolio.id"), nullable=False
    )
    process_version_version: Mapped[str] = mapped_column(
        ForeignKey("process_version.version"), nullable=False
    )

    # relationship
    process_version = relationship("Process_version_model", backref="feasibility")
    process_portfolio = relationship("Process_portfolio_model", backref="feasibility")


class Strategic_importance_model(Base):
    __tablename__ = "strategic_importance"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    total_score: Mapped[float] = mapped_column(nullable=True)

    # foreign key
    process_portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("process_portfolio.id"), nullable=False
    )
    process_version_version: Mapped[str] = mapped_column(
        ForeignKey("process_version.version"), nullable=False
    )

    # relationship
    process_version = relationship(
        "Process_version_model", backref="strategic_importance"
    )
    process_portfolio = relationship(
        "Process_portfolio_model", backref="strategic_importance"
    )


class Process_portfolio_model(Base):
    __tablename__ = "process_portfolio"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    # foreign key
    workspace_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)

    # relationship
    workspace = relationship("Project_model", backref="process_portfolio")


Base.metadata.create_all(DatabaseConnector.get_engine())
