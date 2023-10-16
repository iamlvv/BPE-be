from .utils import *
from .notification import Notification


class Notification:
    id = ""
    userId = ""
    createdAt = datetime.now()
    content = ""
    isDeleted = False
    isStarred = False
    isRead = False

    def __init__(
        self,
        id: str,
        userId: str,
        createdAt: datetime,
        content: str,
        isDeleted: bool,
        isStarred: bool,
        isRead: bool,
    ) -> None:
        self.id = id
        self.userId = userId
        self.createdAt = createdAt
        self.content = content
        self.isDeleted = isDeleted
        self.isStarred = isStarred
        self.isRead = isRead

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
        createdAt: str,
        content: str,
        isDeleted: bool,
        isStarred: bool,
        isRead: bool,
    ) -> Notification | None:
        query = f"""INSERT INTO public.notification
                    ("userId", "createdAt", "content", "isDeleted", "isStarred", "isRead")
                    VALUES('{userId}', '{createdAt}', '{content}', {isDeleted}, {isStarred}, {isRead})
                    RETURNING "id", "userId", "createdAt", "content";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Notification(
                        id=result[0],
                        userId=result[1],
                        createdAt=result[2],
                        content=result[3],
                        isDeleted=result[4],
                        isStarred=result[5],
                        isRead=result[6],
                    )
                else:
                    return None
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def deleteNotification(cls, notificationId: str) -> bool:
        query = f"""UPDATE public.notification
                    SET "isDeleted"=true
                    WHERE "id"='{notificationId}'
                    RETURNING "id", "userId", "createdAt", "content";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def starNotification(cls, notificationId: str) -> bool:
        query = f"""UPDATE public.notification
                    SET "isStarred"=true
                    WHERE "id"='{notificationId}'
                    RETURNING "id", "userId", "createdAt", "content";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getNotifications(cls, userId: str) -> list[Notification]:
        query = f"""SELECT * FROM public.notification
                    WHERE "userId"='{userId}' AND "isDeleted"=false
                    ORDER BY "createdAt" DESC;
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
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getStarredNotifications(cls, userId: str) -> list[Notification]:
        query = f"""SELECT * FROM public.notification
                    WHERE "userId"='{userId}' AND "isDeleted"=false AND "isStarred"=true
                    ORDER BY "createdAt" DESC;
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
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def readNotification(cls, notificationId: str) -> bool:
        query = f"""UPDATE public.notification
                    SET "isRead"=true
                    WHERE "id"='{notificationId}'
                    RETURNING "id", "userId", "createdAt", "content";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")
