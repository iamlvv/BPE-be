from .utils import *
from .request import Request


class Request:
    id = ""
    type = ""
    content = ""
    createdAt = datetime.now()
    status = ""
    isDeleted = False
    isWorkspaceDeleted = False
    workspaceId = ""
    senderId = ""
    handlerId = ""
    recipientId = ""
    fr_permission = ""
    to_permission = ""
    rcp_permission = ""

    def __init__(
        self,
        id: str,
        type: str,
        content: str,
        createdAt: datetime,
        status: str,
        isDeleted: bool,
        isWorkspaceDeleted: bool,
        workspaceId: str,
        senderId: str,
        handlerId: str,
        recipientId: str,
        fr_permission: str,
        to_permission: str,
        rcp_permission: str,
    ) -> None:
        self.id = id
        self.type = type
        self.content = content
        self.createdAt = createdAt
        self.status = status
        self.isDeleted = isDeleted
        self.isWorkspaceDeleted = isWorkspaceDeleted
        self.workspaceId = workspaceId
        self.senderId = senderId
        self.handlerId = handlerId
        self.recipientId = recipientId
        self.fr_permission = fr_permission
        self.to_permission = to_permission
        self.rcp_permission = rcp_permission

    def __str__(self) -> str:
        return f"""Request(
            id={self.id},
            type={self.type},
            content={self.content},
            createdAt={self.createdAt},
            status={self.status},
            isDeleted={self.isDeleted},
            isWorkspaceDeleted={self.isWorkspaceDeleted},
            workspaceId={self.workspaceId},
            senderId={self.senderId},
            handlerId={self.handlerId},
            recipientId={self.recipientId},
            fr_permission={self.fr_permission},
            to_permission={self.to_permission},
            rcp_permission={self.rcp_permission},
        )"""

    @classmethod
    def insertNewRequest(
        cls,
        type: str,
        content: str,
        createdAt: datetime,
        isDeleted: bool,
        isWorkspaceDeleted: bool,
        status: str,
        workspaceId: str,
        senderId: str,
        handlerId: str,
        recipientId: str,
        fr_permission: str,
        to_permission: str,
        rcp_permission: str,
    ) -> Request | None:
        query = f"""INSERT INTO public.request
                    ("type", "content", "createdAt", "status", "isDeleted", "isWorkspaceDeleted", "workspaceId", "senderId", "handlerId", "recipientId", "fr_permission", "to_permission", "rcp_permission")
                    VALUES('{type}', '{content}', '{createdAt}', '{status}', {isDeleted}, {isWorkspaceDeleted}, '{workspaceId}', '{senderId}', '{handlerId}', '{recipientId}', '{fr_permission}', '{to_permission}', '{rcp_permission}')
                    RETURNING "id", "type", "content", "createdAt", "status", "workspaceId", "senderId", "handlerId", "recipientId", "fr_permission", "to_permission", "rcp_permission";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Request(
                        id=result[0],
                        type=result[1],
                        content=result[2],
                        createdAt=result[3],
                        status=result[4],
                        isDeleted=result[5],
                        isWorkspaceDeleted=result[6],
                        workspaceId=result[7],
                        senderId=result[8],
                        handlerId=result[9],
                        recipientId=result[10],
                        fr_permission=result[11],
                        to_permission=result[12],
                        rcp_permission=result[13],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def approveRequest(cls, id: str) -> Request | None:
        query = f"""UPDATE public.request
                    SET "status"='approved'
                    WHERE "id"='{id}'
                    RETURNING "id", "type", "content", "createdAt", "status", "workspaceId", "senderId", "handlerId", "recipientId", "fr_permission", "to_permission", "rcp_permission";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Request(
                        id=result[0],
                        type=result[1],
                        content=result[2],
                        createdAt=result[3],
                        status=result[4],
                        isDeleted=result[5],
                        isWorkspaceDeleted=result[6],
                        workspaceId=result[7],
                        senderId=result[8],
                        handlerId=result[9],
                        recipientId=result[10],
                        fr_permission=result[11],
                        to_permission=result[12],
                        rcp_permission=result[13],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def declineRequest(cls, id: str) -> Request | None:
        query = f"""UPDATE public.request
                    SET "status"='declined'
                    WHERE "id"='{id}'
                    RETURNING "id", "type", "content", "createdAt", "status", "workspaceId", "senderId", "handlerId", "recipientId", "fr_permission", "to_permission", "rcp_permission";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Request(
                        id=result[0],
                        type=result[1],
                        content=result[2],
                        createdAt=result[3],
                        status=result[4],
                        isDeleted=result[5],
                        isWorkspaceDeleted=result[6],
                        workspaceId=result[7],
                        senderId=result[8],
                        handlerId=result[9],
                        recipientId=result[10],
                        fr_permission=result[11],
                        to_permission=result[12],
                        rcp_permission=result[13],
                    )
                else:
                    return None

        except Exception as e:
            connection.rollback()
            raise Exception(e)

    def removeRequest(self, id: str) -> Request | None:
        query = f"""UPDATE public.request
                    SET "isDeleted"=true
                    WHERE "id"='{id}'
                    RETURNING "id", "type", "content", "createdAt", "status", "workspaceId", "senderId", "handlerId", "recipientId", "fr_permission", "to_permission", "rcp_permission";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Request(
                        id=result[0],
                        type=result[1],
                        content=result[2],
                        createdAt=result[3],
                        status=result[4],
                        isDeleted=result[5],
                        isWorkspaceDeleted=result[6],
                        workspaceId=result[7],
                        senderId=result[8],
                        handlerId=result[9],
                        recipientId=result[10],
                        fr_permission=result[11],
                        to_permission=result[12],
                        rcp_permission=result[13],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)
