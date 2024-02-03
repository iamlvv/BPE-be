from datetime import datetime


class WorkspaceModel:
    id: int
    name: str
    description: str
    created_at: datetime
    ownerId: str
    background: str
    icon: str
    isPersonal: bool
    isDeleted: bool
    deletedAt: datetime
