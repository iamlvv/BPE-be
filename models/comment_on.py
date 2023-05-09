from .utils import *


class CommentOn:
    id = 0
    user_id = 0
    project_id = 0
    xml_file_link = ""
    content = ""
    create_at = datetime.now()

    @classmethod
    def insert(self, user_id, project_id, xml_file_link, content):
        query = """INSERT INTO public.comment_on
                    (user_id, project_id, xml_file_link, "content", create_at)
                    VALUES(%s, %s, %s, %s, NOW());
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (user_id, project_id, xml_file_link, content,))
            connection.commit()

    @classmethod
    def update(self, id, content):
        query = """UPDATE public.comment_on
                    SET "content"=%s
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (content, id,))
            if cursor.rowcount == 0:
                raise Exception('update failed')
            connection.commit()

    @classmethod
    def owner(self, user_id, project_id, xml_file_link, id):
        query = """SELECT id
                    FROM public.comment_on
                    WHERE user_id=%s AND project_id=%s AND xml_file_link=%s AND id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (user_id, project_id, xml_file_link, id,))
            return cursor.fetchone() != None

    @classmethod
    def delete(self, id):
        query = """DELETE FROM public.comment_on
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            if cursor.rowcount == 0:
                raise Exception('delete failed')
            connection.commit()

    @classmethod
    def get(self, user_id, project_id, xml_file_link):
        query = """SELECT id, user_id, project_id, xml_file_link, "content", create_at
                    FROM public.comment_on
                    WHERE user_id=%s AND project_id=%s AND xml_file_link=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (user_id, project_id, xml_file_link,))
            return list_tuple_to_dict(["id", "user_id", "project_id", "xml_file_link", "content", "create_at"], cursor.fetchall())

    @classmethod
    def get_by_bpmn_file(self, project_id, xml_file_link):
        query = """SELECT id, user_id, project_id, xml_file_link, "content", create_at
                    FROM public.comment_on
                    WHERE project_id=%s AND xml_file_link=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (project_id, xml_file_link,))
            return list_tuple_to_dict(["id", "user_id", "project_id", "xml_file_link", "content", "create_at"], cursor.fetchall())

    @classmethod
    def get_by_user(self, user_id):
        query = """SELECT id, user_id, project_id, xml_file_link, "content", create_at
                    FROM public.comment_on
                    WHERE user_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (user_id,))
            return list_tuple_to_dict(["id", "user_id", "project_id", "xml_file_link", "content", "create_at"], cursor.fetchall())
