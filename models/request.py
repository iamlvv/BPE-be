from .utils import *
from datetime import date


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

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)
        vars(self).update(kwargs)

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

    def findDuplicateRequest(
        requestType, content, status, createdAt, workspaceId, senderId, recipientId
    ):
        # find duplicate request
        # if createdAt is different, if the discrepancy is less than 1 day, then it is a duplicate request
        query = f"""SELECT createdAt, status
                    FROM public.request
                    WHERE type='{requestType}' AND content='{content}' AND status='{status}' AND workspaceId='{workspaceId}' AND senderId='{senderId}' AND recipientId='{recipientId}' AND isDeleted=false AND isWorkspaceDeleted=false
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    recentCreatedAt = result[0]
                    resultStatus = result[1]
                    if (
                        createdAt - recentCreatedAt
                    ).days < 1 and resultStatus == "pending":
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            raise Exception(e)

    @classmethod
    def getAllRequests(cls, workspaceId, keyword=None, type=None, status=None):
        query = f"""SELECT id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission
                    FROM public.request
                    WHERE workspaceId='{workspaceId}' AND isDeleted=false AND isWorkspaceDeleted=false
                """

        if keyword:
            query += f""" AND content LIKE '%{keyword}%'"""
        if type:
            query += f""" AND type='{type}'"""
        if status:
            query += f""" AND status='{status}'"""

        query += f""" ORDER BY createdAt DESC;"""

        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                if result:
                    requestsList = []
                    for request in result:
                        requestsList.append(
                            Request(
                                id=request[0],
                                type=request[1],
                                content=request[2],
                                createdAt=request[3],
                                status=request[4],
                                workspaceId=request[5],
                                senderId=request[6],
                                handlerId=request[7],
                                recipientId=request[8],
                                fr_permission=request[9],
                                to_permission=request[10],
                                rcp_permission=request[11],
                            )
                        )
                    return requestsList
                else:
                    return []
        except Exception as e:
            raise Exception(e)

    @classmethod
    def insertNewRequest(
        cls,
        requestType,
        content,
        createdAt,
        status,
        workspaceId,
        senderId,
        recipientId,
        handlerId,
        fr_permission,
        to_permission,
        rcp_permission,
    ):
        isDuplicate = Request.findDuplicateRequest(
            requestType, content, status, createdAt, workspaceId, senderId, recipientId
        )
        if isDuplicate:
            return "Duplicate request"

        query = f"""INSERT INTO public.request
                    (type, content, createdAt, status, isDeleted, isWorkspaceDeleted, workspaceId, senderId, recipientId, handlerId, fr_permission, to_permission, rcp_permission)
                    VALUES('{requestType}', '{content}', '{createdAt}', '{status}', false, false, '{workspaceId}', '{senderId}', '{recipientId}', '{handlerId}', '{fr_permission}', '{to_permission}', '{rcp_permission}')
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, recipientId, handlerId, fr_permission, to_permission, rcp_permission;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                print(result)
                if result:
                    return Request(
                        id=result[0],
                        type=result[1],
                        content=result[2],
                        createdAt=result[3],
                        status=result[4],
                        workspaceId=result[5],
                        senderId=result[6],
                        recipientId=result[7],
                        handlerId=result[8],
                        fr_permission=result[9],
                        to_permission=result[10],
                        rcp_permission=result[11],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def approveRequest(cls, id: str, handlerId: str):
        query = f"""UPDATE public.request
                    SET status=approved, handlerId='{handlerId}'
                    WHERE id='{id}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
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
    def declineRequest(cls, id: str, handlerId: str):
        query = f"""UPDATE public.request
                    SET status='declined', handlerId='{handlerId}'
                    WHERE "id"='{id}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
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

    def removeRequest(self, id: str):
        query = f"""UPDATE public.request
                    SET isDeleted=true
                    WHERE id='{id}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
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
