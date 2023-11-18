from .utils import *
from typing import Sequence


class RemoveOwnerFromMemberList:
    @classmethod
    def removeOwnerFromMemberList(cls, workspaceId: str, memberIdList):
        print("this is member id list", memberIdList)
        query = f"""SELECT ownerId FROM public.workspace
                    WHERE workspace.id='{workspaceId}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                ownerId = result[0]
                # print("this is owner id", ownerId)
                if str(ownerId) in memberIdList:
                    memberIdList.remove(str(ownerId))
                    # print("this is member id list after remove", memberIdList)
                return memberIdList
        except Exception as e:
            connection.rollback()
            raise Exception(e)


class Join_Workspace_Get(RemoveOwnerFromMemberList):
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
            query += f""" AND LOWER(u.name) LIKE LOWER('%{keyword}%')"""
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
    def getMember(cls, workspaceId: str, memberId: str):
        query = f"""SELECT memberId, workspaceId, joinedAt, permission, isDeleted FROM public.join_workspace
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
                        isDeleted=result[4],
                    )
                else:
                    return None
        except Exception as e:
            connection.rollback()
            raise Exception(e)


class Join_Workspace_Update(RemoveOwnerFromMemberList):
    @classmethod
    def updatePermission(
        cls, workspaceId, newMemberIdList, currentPermission, newPermission
    ) -> None:
        # memberId is the list of member id
        # update permission of each member in the list
        # return list of members that have been updated
        # first, check if current permission match with permission in database
        # if not, raise exception
        # if yes, update permission
        # return list of members that have been updated
        # print("this is new member id list", newMemberIdList)
        print("this is current permission", currentPermission, newPermission)
        connection = DatabaseConnector.get_connection()
        try:
            for memberId in newMemberIdList:
                query = f"""SELECT permission FROM public.join_workspace
                        WHERE workspaceId='{workspaceId}' AND memberId = '{memberId}';
                    """
                connection = DatabaseConnector.get_connection()
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    print(result)
                    if currentPermission:
                        if result[0] != currentPermission:
                            raise Exception("Current permission does not match")
                    query = f"""UPDATE public.join_workspace
                            SET permission='{newPermission}'
                            WHERE workspaceId='{workspaceId}' AND memberId='{memberId}';
                        """
                    cursor.execute(query)
                    print("update permission")
                    connection.commit()

            # return list of members in tuple but do not have comma in the end that have been updated
            query = f"""SELECT u.name, u.email, u.avatar, jw.memberId, jw.workspaceId, jw.joinedAt, jw.permission
                        FROM public.join_workspace jw, public.bpe_user u
                        WHERE jw.workspaceId='{workspaceId}' AND jw.memberId IN ({','.join(newMemberIdList)}) AND u.id = jw.memberId;
                    """

            connection = DatabaseConnector.get_connection()
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
    def deleteMember(cls, workspaceId: str, newMemberList, leftAt) -> None:
        for memberId in newMemberList:
            query = f"""UPDATE public.join_workspace
                    SET isDeleted=true, leftAt = '{leftAt}'
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
        return "Delete member successfully"

    @classmethod
    def undoDeleteMember(cls, workspaceId, memberIdList):
        for memberId in memberIdList:
            query = f"""UPDATE public.join_workspace
                    SET isDeleted=false, leftAt = null
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


class Join_Workspace_Insert(RemoveOwnerFromMemberList):
    @classmethod
    def insertNewMember(
        cls,
        memberId: str,
        workspaceId: str,
        joinedAt: str,
        permission: str,
        isDeleted: bool,
    ):
        print("this is isDeleted in models", isDeleted)
        if isDeleted:
            query = f"""UPDATE public.join_workspace
                        SET isDeleted=false, joinedAt='{joinedAt}', permission='{permission}'
                        WHERE memberId='{memberId}' AND workspaceId='{workspaceId}'
                        RETURNING memberId, workspaceId, joinedAt, permission;
                    """
            connection = DatabaseConnector.get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    connection.commit()
                    # return the updated member
                    query = f"""SELECT u.name, u.email, u.avatar, jw.memberId, jw.workspaceId, jw.joinedAt, jw.permission
                            FROM public.join_workspace jw, public.bpe_user u
                            WHERE jw.memberId='{memberId}' AND jw.workspaceId='{workspaceId}' AND u.id = jw.memberId;
                        """
                    cursor.execute(query)
                    result = cursor.fetchone()
                    return {
                        "name": result[0],
                        "email": result[1],
                        "avatar": result[2],
                        "memberId": result[3],
                        "workspaceId": result[4],
                        "joinedAt": result[5],
                        "permission": result[6],
                    }

            except Exception as e:
                connection.rollback()
                raise Exception(e)
        else:
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
                    # return the inserted member including name, email, avatar, joinedAt, permission, memberId, workspaceId
                    if result:
                        query = f"""SELECT u.name, u.email, u.avatar, jw.memberId, jw.workspaceId, jw.joinedAt, jw.permission
                                FROM public.join_workspace jw, public.bpe_user u
                                WHERE jw.memberId='{memberId}' AND jw.workspaceId='{workspaceId}' AND u.id = jw.memberId;
                            """
                        cursor.execute(query)
                        result = cursor.fetchone()
                        return {
                            "name": result[0],
                            "email": result[1],
                            "avatar": result[2],
                            "memberId": result[3],
                            "workspaceId": result[4],
                            "joinedAt": result[5],
                            "permission": result[6],
                        }
                    else:
                        return None

            except Exception as e:
                connection.rollback()
                raise Exception(e)


class Join_Workspace(Join_Workspace_Get, Join_Workspace_Insert, Join_Workspace_Update):
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
