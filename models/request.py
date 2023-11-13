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
        # if after sending request, user be kicked out of workspace, then the request is deleted, so it is not a duplicate request
        # if createdAt is different, if the discrepancy is less than 1 day, then it is a duplicate request
        query = f"""SELECT r.createdAt, r.status, jw.isDeleted
                    FROM public.request r, public.join_workspace jw
                    WHERE r.type='{requestType}' AND r.content='{content}' AND r.status='{status}' 
                    AND r.workspaceId='{workspaceId}' AND r.senderId='{senderId}' AND r.recipientId='{recipientId}' 
                    AND r.isDeleted=false AND r.isWorkspaceDeleted=false AND jw.memberId='{senderId}'
                    AND r.workspaceId=jw.workspaceId
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    recentCreatedAt = result[0]
                    resultStatus = result[1]
                    isDeleted = result[2]
                    print(recentCreatedAt, resultStatus, isDeleted)
                    if (
                        (createdAt - recentCreatedAt).days < 1
                        and resultStatus == "pending"
                        and isDeleted == False
                    ):
                        return True
                    else:
                        return False
                else:
                    return False
        except Exception as e:
            raise Exception(e)

    @classmethod
    def getAllRequests(
        cls, workspaceId, page, limit, keyword=None, type=None, status=None
    ):
        query = f"""SELECT id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission
                    FROM public.request
                    WHERE workspaceId='{workspaceId}' AND isDeleted=false AND isWorkspaceDeleted=false
                """

        if keyword:
            query += f""" AND LOWER(content) LIKE LOWER('%{keyword}%')"""
        if type:
            query += f""" AND type='{type}'"""
        if status:
            query += f""" AND status='{status}'"""

        query += f""" ORDER BY createdAt DESC"""

        total = 0

        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                total = len(result)

                if page and limit:
                    page = int(page)
                    limit = int(limit)
                    query += f""" LIMIT {limit} OFFSET {(page-1 if page-1 >= 0 else 0)*limit}"""

                cursor.execute(query)
                result = cursor.fetchall()

                if result:
                    return {
                        "total": total,
                        "limit": limit,
                        "data": [
                            Request(
                                id=item[0],
                                type=item[1],
                                content=item[2],
                                createdAt=item[3],
                                status=item[4],
                                workspaceId=item[5],
                                senderId=item[6],
                                handlerId=item[7],
                                recipientId=item[8],
                                fr_permission=item[9],
                                to_permission=item[10],
                                rcp_permission=item[11],
                            )
                            for item in result
                        ],
                    }
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
        print(
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
        )
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
    def approveRequest(cls, workspaceId, requestIdList, handlerId):
        result = []
        for requestId in requestIdList:
            query = f"""UPDATE public.request
                        SET status='approved', handlerId='{handlerId}'
                        WHERE id='{requestId}' AND workspaceId='{workspaceId}'
                        RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
                    """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    result.append(cursor.fetchone())
            except Exception as e:
                connection.rollback()
                raise Exception(e)
        return result

    @classmethod
    def declineRequest(cls, workspaceId, requestIdList, handlerId):
        result = []
        for requestId in requestIdList:
            query = f"""UPDATE public.request
                    SET status='declined', handlerId='{handlerId}'
                    WHERE "id"='{requestId}' AND workspaceId='{workspaceId}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    result.append(cursor.fetchone())
            except Exception as e:
                connection.rollback()
                raise Exception(e)

        return result

    @classmethod
    def deleteRequests(cls, workspaceId, requestIdList, deletedAt):
        for requestId in requestIdList:
            query = f"""UPDATE public.request
                    SET isDeleted=true, deletedAt='{deletedAt}'
                    WHERE id='{requestId}' AND workspaceId='{workspaceId}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()

            except Exception as e:
                connection.rollback()
                raise Exception(e)

        return "Delete requests successfully"

    @classmethod
    def deleteRequestsWhenDeletingUser(cls, workspaceId, newMemberList, deletedAt):
        for memberId in newMemberList:
            query = f"""UPDATE public.request
                    SET isDeleted=true, deletedAt='{deletedAt}'
                    WHERE workspaceId='{workspaceId}' AND senderId = '{memberId}'
                    RETURNING id, type, content, createdAt, status, workspaceId, senderId, handlerId, recipientId, fr_permission, to_permission, rcp_permission;
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()

            except Exception as e:
                connection.rollback()
                raise Exception(e)

        return "Delete requests successfully"
