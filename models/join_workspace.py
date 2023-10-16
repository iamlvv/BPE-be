from .utils import *
from typing import Sequence


class Join_Workspace:
    memberId = ""
    workspaceId = ""
    joinedAt = datetime.now()
    permission = ""
    isDeleted = False
    isWorkspaceDeleted = False

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)
        vars(self).update(kwargs)

    def __str__(self):
        return f"""Join_Workspace(
            memberId={self.memberId},
            workspaceId={self.workspaceId},
            joinedAt={self.joinedAt},
            permission={self.permission},
            isDeleted={self.isDeleted},
            isWorkspaceDeleted={self.isWorkspaceDeleted},
        )"""

    @classmethod
    def insertNewMember(
        cls, memberId: str, workspaceId: str, joinedAt: str, permission: str
    ):
        query = f"""INSERT INTO public.join_workspace
                    ("memberId", "workspaceId", "joinedAt", "permission", "isDeleted", "isWorkspaceDeleted")
                    VALUES('{memberId}', '{workspaceId}', '{joinedAt}', '{permission}', false, false)
                    RETURNING "memberId", "workspaceId", "joinedAt", "permission";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Join_Workspace(
                        memberId=result[0],
                        workspaceId=result[1],
                        joinedAt=result[2],
                        permission=result[3],
                    )
                else:
                    return None
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getAllMembers(cls, workspaceId: str):
        query = f"""SELECT * FROM public.join_workspace
                    WHERE "workspaceId" = {workspaceId} AND "isDeleted"=false AND "isWorkspaceDeleted"=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [
                    Join_Workspace(
                        memberId=result[0],
                        workspaceId=result[1],
                        joinedAt=result[2],
                        permission=result[3],
                    )
                    for result in results
                ]
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def updatePermission(cls, workspaceId: str, memberId: str, permission: str) -> None:
        query = f"""UPDATE public.join_workspace
                    SET "permission"='{permission}'
                    WHERE "workspaceId"='{workspaceId}' AND "memberId"='{memberId}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def deleteMember(cls, workspaceId: str, memberId: str) -> None:
        query = f"""UPDATE public.join_workspace
                    SET "isDeleted"=true
                    WHERE "workspaceId"='{workspaceId}' AND "memberId"='{memberId}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")
