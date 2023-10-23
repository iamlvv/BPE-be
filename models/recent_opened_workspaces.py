from .utils import *
import json


class Recent_Opened_Workspaces:
    workspaceId = ""
    userId = ""
    openedAt = ""
    isHided = False
    isPinned = False
    isWorkspaceDeleted = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    @classmethod
    def insert(cls, workspaceId, userId, openedAt):
        query = f"""INSERT INTO public.recent_opened_workspace
                    (workspaceId, userId, openedAt, isHided, isPinned, isWorkspaceDeleted)
                    VALUES('{workspaceId}', '{userId}', '{openedAt}', false, false, false)
                    RETURNING workspaceId, userId, openedAt;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return Recent_Opened_Workspaces(
                    workspaceId=result[0],
                    userId=result[1],
                    openedAt=result[2],
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def hideOpenedWorkspace(cls, workspaceId, userId):
        query = f"""UPDATE public.recent_opened_workspace
                    SET isHided=true
                    WHERE workspaceId='{workspaceId}' AND userId='{userId}'
                    RETURNING workspaceId, userId, openedAt;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return "Hided workspace successfully"
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def pinOpenedWorkspace(cls, workspaceId, userId):
        query = f"""UPDATE public.recent_opened_workspace
                    SET isPinned=true
                    WHERE workspaceId='{workspaceId}' AND userId='{userId}'
                    RETURNING workspaceId, userId;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                return "Pinned workspace successfully"
        except Exception as e:
            connection.rollback()
            raise Exception(e)