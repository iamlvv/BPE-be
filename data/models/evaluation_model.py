from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.meta_data import Base
from data.models.process_model import Process_version_model
from database.db import DatabaseConnector


class Evaluation_result_model(Base):
    __tablename__ = "evaluated_result"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    create_at: Mapped[str] = mapped_column(nullable=False)

    # result: type jsonb
    result = Column(JSONB)

    # foreign key
    xml_file_link: Mapped[str] = mapped_column(
        ForeignKey("process_version.xml_file_link"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("process_version.project_id"), nullable=False
    )
    process_version_version: Mapped[str] = mapped_column(
        ForeignKey("process_version.version"), nullable=True, unique=True
    )
    process_id: Mapped[int] = mapped_column(
        ForeignKey("process_version.process_id"), nullable=False
    )

    project = relationship(
        "Process_version_model",
        foreign_keys=[project_id],
        backref="evaluation_result_project",
    )
    process = relationship(
        "Process_version_model",
        foreign_keys=[process_id],
        backref="evaluation_result_process",
    )
    process_version = relationship(
        "Process_version_model",
        foreign_keys=[process_version_version],
        backref="evaluation_result_process_version",
    )
    xml_file = relationship(
        "Process_version_model",
        foreign_keys=[xml_file_link],
        backref="evaluation_result_xml_file",
    )


# Base.metadata.create_all(DatabaseConnector.get_engine())
