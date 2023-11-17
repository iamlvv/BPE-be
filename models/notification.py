from .utils import *
import json
from bpsky import socketio


class Notification:
    id = ""
    userId = ""
    createdAt = datetime.now()
    content = ""
    isDeleted = False
    isStarred = False
    isRead = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    def __str__(self) -> str:
        return f"""Notification(
            id={self.id},
            userId={self.userId},
            createdAt={self.createdAt},
            content={self.content},
            isDeleted={self.isDeleted},
            isStarred={self.isStarred},
            isRead={self.isRead},
        )"""

    @classmethod
    def insertNewNotification(
        cls,
        userId: str,
        content: str,
        createdAt: str,
        isDeleted: bool,
        isStarred: bool,
        isRead: bool,
    ):
        query = f"""INSERT INTO public.notification
                    (userId, createdAt, content, isDeleted, isStarred, isRead)
                    VALUES('{userId}', '{createdAt}', '{content}', {isDeleted}, {isStarred}, {isRead})
                    RETURNING id, userId, createdAt, content, isRead;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    # only emit to the user who is being notified
                    socketio.emit(
                        "insertNewNotification_" + str(userId),
                        json.dumps(
                            {
                                "id": result[0],
                                "userId": result[1],
                                "createdAt": result[2],
                                "content": result[3],
                                "isRead": result[4],
                            },
                            default=str,
                        ),
                    )
                    return Notification(
                        id=result[0],
                        userId=result[1],
                        createdAt=result[2],
                        content=result[3],
                        isRead=result[4],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def deleteNotification(cls, notificationIdList, deletedAt):
        for notificationId in notificationIdList:
            query = f"""UPDATE public.notification
                    SET isDeleted=true, deletedAt='{deletedAt}'
                    WHERE id='{notificationId}'
                    RETURNING id, userId, createdAt, content;
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    # result = cursor.fetchone()
            except Exception as e:
                connection.rollback()
                raise Exception(e)

        return "Delete notification successfully"

    @classmethod
    def starNotification(cls, notificationId: str):
        query = f"""UPDATE public.notification
                    SET isStarred=true
                    WHERE id='{notificationId}' AND isDeleted=false
                    RETURNING id, userId, createdAt, content, isStarred, isRead;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return Notification(
                    id=result[0],
                    userId=result[1],
                    createdAt=result[2],
                    content=result[3],
                    isStarred=result[4],
                    isRead=result[5],
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def getAllNotifications(cls, userId, page, limit, isStarred, keyword=None):
        query = f"""SELECT id, userId, createdAt, content, isStarred, isRead FROM public.notification
                    WHERE userId='{userId}' AND isDeleted=false
                """
        if isStarred:
            query += " AND isStarred=true"
        if keyword:
            query += f" AND LOWER(content) LIKE LOWER('%{keyword}%')"
        query += " ORDER BY createdAt DESC"
        total = 0

        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                total = len(results)
                if page and limit:
                    page = int(page)
                    limit = int(limit)
                    query += f""" LIMIT {limit} OFFSET {(page-1 if page-1 >= 0 else 0)*limit}"""

                cursor.execute(query)
                results = cursor.fetchall()
                return {
                    "total": total,
                    "limit": limit,
                    "data": [
                        Notification(
                            id=result[0],
                            userId=result[1],
                            createdAt=result[2],
                            content=result[3],
                            isStarred=result[4],
                            isRead=result[5],
                        )
                        for result in results
                    ],
                }
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def getStarredNotifications(cls, userId: str):
        query = f"""SELECT * FROM public.notification
                    WHERE userId='{userId}' AND isDeleted=false AND isStarred=true
                    ORDER BY createdAt DESC;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [
                    Notification(
                        id=result[0],
                        userId=result[1],
                        createdAt=result[2],
                        content=result[3],
                        isDeleted=result[4],
                        isStarred=result[5],
                        isRead=result[6],
                    )
                    for result in results
                ]
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def readNotification(cls, notificationId: str):
        query = f"""UPDATE public.notification
                    SET isRead=true
                    WHERE id='{notificationId}'
                    RETURNING id, userId, createdAt, content, isRead, isStarred;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return Notification(
                    id=result[0],
                    userId=result[1],
                    createdAt=result[2],
                    content=result[3],
                    isRead=result[4],
                    isStarred=result[5],
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)
