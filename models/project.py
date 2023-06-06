from .utils import *


class Project:
    id = 0
    description = ""
    name = ""
    is_delete = False
    create_at = datetime.now()

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    @classmethod
    def create(cls, description, name):
        query = """INSERT INTO public.project
                    (description, "name", is_delete, create_at)
                    VALUES(%s, %s, false, NOW())
                    RETURNING id, description, "name";
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (description, name,))
                connection.commit()
                result = cursor.fetchone()
                return Project(id=result[0], description=result[1], name=result[2])
        except:
            connection.rollback()

    @classmethod
    def get(self, project_id):
        query = """SELECT project.id, description, "name", create_at, work_on.user_id
                    FROM public.project, public.work_on
                    WHERE project.id=%s AND is_delete=false AND project.id=work_on.project_id;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (project_id,))
                connection.commit()
                result = cursor.fetchone()
                return {
                    'id': result[0],
                    'name': result[1],
                    'description': result[2],
                    'create_at': result[3],
                    'user_id': result[4]
                }
        except:
            connection.rollback()

    @classmethod
    def delete(self, project_id):
        query = """UPDATE public.project
                    SET is_delete=true
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (project_id,))
                connection.commit()
        except:
            connection.rollback()

    @classmethod
    def get_all(cls):
        query = """SELECT id, description, "name", create_at
                    FROM public.project
                    WHERE is_delete=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchall()
                return list_tuple_to_dict(["id", "description", "name", "create_at"], result)
        except:
            connection.rollback()

    @classmethod
    def update_name(self, project_id, name):
        query = """UPDATE public.project
                    SET "name"=%s
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (name, project_id,))
                connection.commit()
                updated_row = cursor.rowcount
                if updated_row == 0:
                    raise Exception('project id incorrect')
        except:
            connection.rollback()

    @classmethod
    def update_description(self, project_id, description):
        query = """UPDATE public.project
                    SET description=%s
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (description, project_id,))
                connection.commit()
                updated_row = cursor.rowcount
                if updated_row == 0:
                    raise Exception('project id incorrect')
        except:
            connection.rollback()

    @classmethod
    def get_all_project_by_project_ids(self, project_ids):
        query = f"""SELECT id, description, "name", create_at
                    FROM public.project
                    WHERE id IN ({",".join(str(project_id) for project_id in project_ids)}) AND is_delete=false
                    ORDER BY create_at;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                result = cursor.fetchall()
                return list_tuple_to_dict(["id", "description", "name", "create_at"], result)
        except:
            connection.rollback()
