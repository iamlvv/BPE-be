from .utils import *
import json


class Workspace:
    id = 0
    name = ""
    description = ""
    createdAt = datetime.now()
    ownerId = ""
    background = ""
    icon = ""
    isPersonal = False
    isDeleted = False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    @classmethod
    def insertNewWorkspace(
        cls,
        name: str,
        description: str,
        createdAt: datetime,
        ownerId: str,
        background: str,
        icon: str,
        isPersonal: bool,
        isDeleted: bool,
    ):
        query = f"""INSERT INTO public.workspace
                    (name, description, createdAt, ownerId, background, icon, isPersonal, isDeleted)
                    VALUES('{name}', '{description}', '{createdAt}', '{ownerId}', '{background}', '{icon}', '{isPersonal}', '{isDeleted}')
                    RETURNING id, name, description, createdAt, ownerId, background, icon, isPersonal, isDeleted;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchone()
                if result:
                    return Workspace(
                        id=result[0],
                        name=result[1],
                        description=result[2],
                        createdAt=result[3],
                        ownerId=result[4],
                        background=result[5],
                        icon=result[6],
                        isPersonal=result[7],
                        isDeleted=result[8],
                    )
                else:
                    return None

        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def deleteWorkspace(cls, id: str) -> bool:
        query = f"""UPDATE public.workspace
                    SET "isDeleted"=true
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def updateWorkspaceDescriptions(cls, id: str, description: str) -> bool:
        query = f"""UPDATE public.workspace
                    SET "description"='{description}'
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def updateWorkspaceName(cls, id: str, name: str) -> bool:
        query = f"""UPDATE public.workspace
                    SET "name"='{name}'
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def updateWorkspaceBackground(cls, id: str, background: str) -> bool:
        query = f"""UPDATE public.workspace
                    SET "background"='{background}'
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def updateWorkspaceIcon(cls, id: str, icon: str) -> bool:
        query = f"""UPDATE public.workspace
                    SET "icon"='{icon}'
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return True
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getWorkspace(cls, id: str):
        query = f"""SELECT id, name, description, createdAt, "ownerId", background, icon, "isPersonal", "isDeleted"
                    FROM public.workspace
                    WHERE id='{id}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return Workspace(
                        id=result[0],
                        name=result[1],
                        description=result[2],
                        createdAt=result[3],
                        ownerId=result[4],
                        background=result[5],
                        icon=result[6],
                        isPersonal=result[7],
                        isDeleted=result[8],
                    )
                else:
                    return None
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getWorkspaceByOwnerId(cls, ownerId: str) -> list:
        query = f"""SELECT id, name, description, createdAt, "ownerId", background, icon, "isPersonal", "isDeleted"
                    FROM public.workspace
                    WHERE "ownerId"='{ownerId}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(
                    [
                        "id",
                        "name",
                        "description",
                        "createdAt",
                        "ownerId",
                        "background",
                        "icon",
                        "isPersonal",
                        "isDeleted",
                    ],
                    result,
                )
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")

    @classmethod
    def getWorkspaceByOwnerIdAndIsPersonal(cls, ownerId: str, isPersonal: bool) -> list:
        query = f"""SELECT id, name, description, createdAt, "ownerId", background, icon, "isPersonal", "isDeleted"
                    FROM public.workspace
                    WHERE "ownerId"='{ownerId}' AND "isPersonal"='{isPersonal}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(
                    [
                        "id",
                        "name",
                        "description",
                        "createdAt",
                        "ownerId",
                        "background",
                        "icon",
                        "isPersonal",
                        "isDeleted",
                    ],
                    result,
                )
        except:
            connection.rollback()
            raise Exception("oops, something went wrong")
