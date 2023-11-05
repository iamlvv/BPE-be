from .utils import *
from typing import Sequence


class Join_Workspace:
    memberId = ""
    workspaceId = ""
    joinedAt = datetime.now()
    leftAt = datetime.now()
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
                    (memberId, workspaceId, joinedAt, permission, isDeleted, isWorkspaceDeleted)
                    VALUES('{memberId}', '{workspaceId}', '{joinedAt}', '{permission}', false, false)
                    RETURNING memberId, workspaceId, joinedAt, permission;
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
                    return "something wrong"
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def getAllMembers(
        cls, workspaceId: str, page: int, limit: int, keyword=None, permission=None
    ):
        print(limit, page)
        query = f"""SELECT u.name, u.email, u.avatar, jw.memberId, jw.workspaceId, jw.joinedAt, jw.permission
                    FROM public.join_workspace jw, public.bpe_user u
                    WHERE jw.workspaceId = {workspaceId} AND jw.isDeleted=false AND jw.isWorkspaceDeleted=false AND u.id = jw.memberId
                """

        if keyword:
            query += f""" AND u.name LIKE '%{keyword}%'"""
        if permission:
            query += f""" AND jw.permission='{permission}'"""

        query += f""" ORDER BY jw.joinedAt DESC"""
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
                        {
                            "name": result[0],
                            "email": result[1],
                            "avatar": result[2],
                            "memberId": result[3],
                            "workspaceId": result[4],
                            "joinedAt": result[5],
                            "permission": result[6],
                        }
                        for result in results
                    ],
                }

        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def updatePermission(cls, workspaceId, memberIdList, permission) -> None:
        # memberId is the list of member id
        # update permission of each member in the list
        # return list of members that have been updated

        for memberId in memberIdList:
            query = f"""UPDATE public.join_workspace
                        SET permission='{permission}'
                        WHERE workspaceId='{workspaceId}' AND memberId='{memberId}';
                    """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()

            except Exception as e:
                connection.rollback()
                raise Exception(e)

        # return list of members in tuple but do not have comma in the end that have been updated
        query = f"""SELECT u.name, u.email, u.avatar, jw.memberId, jw.workspaceId, jw.joinedAt, jw.permission
                    FROM public.join_workspace jw, public.bpe_user u
                    WHERE jw.workspaceId='{workspaceId}' AND jw.memberId IN ({','.join(memberIdList)}) AND u.id = jw.memberId;
                """

        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return [
                    {
                        "name": result[0],
                        "email": result[1],
                        "avatar": result[2],
                        "memberId": result[3],
                        "workspaceId": result[4],
                        "joinedAt": result[5],
                        "permission": result[6],
                    }
                    for result in results
                ]
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def deleteMember(cls, workspaceId: str, memberIdList) -> None:
        for memberId in memberIdList:
            query = f"""UPDATE public.join_workspace
                    SET isDeleted=true
                    WHERE workspaceId='{workspaceId}' AND memberId='{memberId}';
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    return "Delete member successfully"
            except Exception as e:
                connection.rollback()
                raise Exception(e)

    @classmethod
    def undoDeleteMember(cls, workspaceId, memberIdList):
        for memberId in memberIdList:
            query = f"""UPDATE public.join_workspace
                    SET isDeleted=false
                    WHERE workspaceId='{workspaceId}' AND memberId='{memberId}';
                """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    return "Undo delete member successfully"
            except Exception as e:
                connection.rollback()
                raise Exception(e)

    @classmethod
    def getMember(cls, workspaceId: str, memberId: str):
        query = f"""SELECT * FROM public.join_workspace
                    WHERE join_workspace.workspaceId='{workspaceId}' AND join_workspace.memberId='{memberId}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
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
        except Exception as e:
            connection.rollback()
            raise Exception(e)
