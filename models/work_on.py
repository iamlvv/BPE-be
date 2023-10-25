from .utils import *
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
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        user_id,
                        project_id,
                        role,
                    ),
                )
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def insert_many(self, users, project_id):
        values = ",".join(
            "(%s, %s, %s)" % (user["user_id"], project_id, user["role"])
            for user in users
        )
        query = f"""INSERT INTO public.work_on
                    (user_id, project_id, "role")
                    VALUES{values};
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def update_role(self, user_id, project_id, new_role):
        query = f"""UPDATE public.work_on
                    SET "role"={new_role}
                    WHERE user_id={user_id} AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def update_many_role(self, users, project_id):
        query = ""
        for user in users:
            query += f"""UPDATE public.work_on
                    SET "role"={user["role"]}
                    WHERE user_id={user["user_id"]} AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def delete_many(self, user_ids, project_id):
        query = f"""DELETE FROM public.work_on
                    WHERE user_id IN ({",".join(str(user_id) for user_id in user_ids)}) AND project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_all_project_by_user_id(self, user_id):
        query = f"""SELECT project.id, project.description, project."name", project.create_at,
                            wo."role",
                            bpe_user.id, bpe_user.email, bpe_user.name, bpe_user.phone, bpe_user.avatar
                    FROM work_on wo, work_on wo2, bpe_user, project
                    WHERE wo.user_id={user_id} AND wo.project_id=wo2.project_id AND
                        wo2."role"=0 AND bpe_user.id=wo2.user_id AND project.id = wo.project_id
                        AND project.is_delete=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = []
                for record in cursor.fetchall():
                    prj = dict(
                        zip(
                            ["id", "description", "name", "create_at", "role"],
                            record[:5],
                        )
                    )
                    user = dict(
                        zip(["id", "email", "name", "phone", "avatar"], record[5:])
                    )
                    prj["owner"] = user
                    result.append(prj)
                return result
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_all_owned_project_by_user_id(self, user_id):
        query = f"""SELECT project.id, project.description, project."name", project.create_at,
                            wo."role",
                            bpe_user.id, bpe_user.email, bpe_user.name, bpe_user.phone, bpe_user.avatar
                    FROM work_on wo, work_on wo2, bpe_user, project
                    WHERE wo.user_id={user_id} AND wo.project_id=wo2.project_id AND
                        wo2."role"=0 AND bpe_user.id=wo2.user_id AND project.id = wo.project_id
                        AND project.is_delete=false AND wo.role=0;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = []
                for record in cursor.fetchall():
                    prj = dict(
                        zip(
                            ["id", "description", "name", "create_at", "role"],
                            record[:5],
                        )
                    )
                    user = dict(
                        zip(["id", "email", "name", "phone", "avatar"], record[5:])
                    )
                    prj["owner"] = user
                    result.append(prj)
                return result
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_all_shared_project_by_user_id(self, user_id):
        query = f"""SELECT project.id, project.description, project."name", project.create_at,
                            wo."role",
                            bpe_user.id, bpe_user.email, bpe_user.name, bpe_user.phone, bpe_user.avatar
                    FROM work_on wo, work_on wo2, bpe_user, project
                    WHERE wo.user_id={user_id} AND wo.project_id=wo2.project_id AND
                        wo2."role"=0 AND bpe_user.id=wo2.user_id AND project.id = wo.project_id
                        AND project.is_delete=false AND wo.role=!0;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = []
                for record in cursor.fetchall():
                    prj = dict(
                        zip(
                            ["id", "description", "name", "create_at", "role"],
                            record[:5],
                        )
                    )
                    user = dict(
                        zip(["id", "email", "name", "phone", "avatar"], record[5:])
                    )
                    prj["owner"] = user
                    result.append(prj)
                return result
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_all_user_by_project_id(self, project_id):
        query = f"""SELECT bpe_user.id, bpe_user.email, name, phone, avatar, role
                    FROM public.work_on
                        JOIN public.bpe_user ON work_on.user_id = bpe_user.id
                    WHERE project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(
                    ["id", "email", "name", "phone", "avatar", "role"], result
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def is_not_exists(self, user_ids, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id IN ({",".join(str(user_id) for user_id in user_ids)});
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return len(result) == 0
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def is_exists(self, user_ids, project_id):
        query = f"""SELECT id
                    FROM public.work_on
                    WHERE project_id={project_id} AND user_id IN ({",".join(str(user_id) for user_id in user_ids)});
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return len(result) == len(user_ids)
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def is_project_owner(self, user_id, project_id):
        query = f"""SELECT work_on.id
                    FROM public.work_on
                        JOIN public.project ON work_on.project_id=project.id
                    WHERE project_id={project_id} AND user_id={user_id} AND role={Role.OWNER.value} AND project.is_delete=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result != None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def can_edit(self, user_id, project_id):
        query = f"""SELECT work_on.id
                    FROM public.work_on
                        JOIN public.project ON work_on.project_id=project.id
                    WHERE project_id={project_id} AND user_id={user_id}
                        AND role IN ({Role.OWNER.value}, {Role.CAN_EDIT.value}) AND project.is_delete=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result != None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def can_share(self, user_id, project_id):
        query = f"""SELECT work_on.id
                    FROM public.work_on
                        JOIN public.project ON work_on.project_id=project.id
                    WHERE project_id={project_id} AND user_id={user_id}
                        AND role IN ({Role.OWNER.value}, {Role.CAN_EDIT.value}, {Role.CAN_SHARE.value}) AND project.is_delete=false;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result != None
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def can_view(self, user_id, project_id):
        query = f"""SELECT public.work_on.id
                    FROM public.work_on, public.project
                    WHERE project.id=work_on.project_id AND project.is_delete=false AND work_on.project_id={project_id} AND work_on.user_id={user_id}
                    AND role IN ('{Role.OWNER.value}', '{Role.CAN_EDIT.value}', '{Role.CAN_SHARE.value}', '{Role.CAN_VIEW.value}') AND project.is_delete=false;

                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                print("result", result)
                if result:
                    return True
                else:
                    return False
        except Exception as e:
            connection.rollback()
            raise Exception(e)
