from .utils import *
from .user import User
from .constant import Role


class WorkOn:
    user_id = 0
    project_id = 0
    role = 0

    @classmethod
    def insert(self, user_id, project_id, role):
        query = """INSERT INTO public.work_on
                    (user_id, project_id, "role")
                    VALUES(%s, %s, %s);
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id, project_id, role,))
            connection.commit()

    @classmethod
    def insert_many(self, user_ids, project_id, role):
        values = ",".join("(%s, %s, %s)" %
                          (id, project_id, role) for id in user_ids)
        query = f"""INSERT INTO public.work_on
                    (user_id, project_id, "role")
                    VALUES{values};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def update_role(self, user_id, project_id, new_role):
        query = f"""UPDATE public.work_on
                    SET "role"={new_role}
                    WHERE user_id={user_id} AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def update_many_role(self, user_ids, project_id, new_role):
        query = f"""UPDATE public.work_on
                    SET "role"={new_role}
                    WHERE user_id IN ({",".join(str(user_id) for user_id in user_ids)}) AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def delete_many(self, user_ids, project_id):
        query = f"""DELETE FROM public.work_on
                    WHERE user_id IN ({",".join(str(user_id) for user_id in user_ids)}) AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def get_all_project_by_user_id(self, user_id):
        query = f"""SELECT project.id, project.description, project."name", project.create_at
                    FROM public.work_on
                        JOIN public.project ON work_on.project_id = project.id
                    WHERE user_id={user_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return list_tuple_to_dict(["id", "description", "name", "create_at"], result)

    @classmethod
    def get_all_user_by_project_id(self, project_id):
        query = f"""SELECT name, phone, avatar
                    FROM public.work_on
                        JOIN public.bpe_user ON work_on.user_id = bpe_user.id
                    WHERE project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return list_tuple_to_dict(["name", "phone", "avatar"], result)

    @classmethod
    def is_not_exists(self, user_ids, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id IN ({",".join(str(user_id) for user_id in user_ids)});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return len(result) == 0

    @classmethod
    def is_exists(self, user_ids, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id IN ({",".join(str(user_id) for user_id in user_ids)});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return len(result) == len(user_ids)

    @classmethod
    def is_project_owner(self, user_id, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id={user_id} AND role={Role.OWNER.value};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result != None

    @classmethod
    def can_edit(self, user_id, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id={user_id}
                        AND role IN ({Role.OWNER.value}, {Role.CAN_EDIT.value});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result != None

    @classmethod
    def can_share(self, user_id, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id={user_id}
                        AND role IN ({Role.OWNER.value}, {Role.CAN_EDIT.value}, {Role.CAN_SHARE.value});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result != None

    @classmethod
    def can_view(self, user_id, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id={user_id}
                        AND role IN ({Role.OWNER.value}, {Role.CAN_EDIT.value}, {Role.CAN_SHARE.value}, {Role.CAN_VIEW.value});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result != None
