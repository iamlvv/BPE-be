from datetime import datetime


class ProjectModel:
    id: int
    description: str
    name: str
    is_delete: bool
    create_at: datetime
    ownerId: str
    workspaceId: str
    deletedAt = datetime
    isWorkspaceDeleted: bool

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)
