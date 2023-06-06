from .utils import *


class CommentOn:
    id = 0
    user_id = 0
    project_id = 0
    process_id = 0
    xml_file_link = ""
    content = ""
    create_at = datetime.now()

    @classmethod
    def insert(self, user_id, project_id, process_id, xml_file_link, content):
        query = """INSERT INTO public.comment_on
                    (user_id, project_id, process_id, xml_file_link, "content", create_at)
                    VALUES(%s, %s, %s, %s, %s, NOW())
                    RETURNING user_id, project_id, xml_file_link, "content", create_at;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (user_id, project_id, process_id, xml_file_link, content,))
                connection.commit()
                result = cursor.fetchone()
                return dict(zip(["user_id", "project_id", "process_id", "xml_file_link", "content", "create_at"], result))

    @classmethod
    def update(self, id, content):
        query = """UPDATE public.comment_on
                    SET "content"=%s
                    WHERE id=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (content, id,))
                if cursor.rowcount == 0:
                    raise Exception('update failed')
                connection.commit()

    @classmethod
    def owner(self, user_id, project_id, process_id, xml_file_link, id):
        query = """SELECT id
                    FROM public.comment_on
                    WHERE user_id=%s AND project_id=%s AND xml_file_link=%s AND id=%s AND process_id=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (user_id, project_id, xml_file_link, id, process_id,))
                return cursor.fetchone() != None

    @classmethod
    def delete(self, id):
        query = """DELETE FROM public.comment_on
                    WHERE id=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                if cursor.rowcount == 0:
                    raise Exception('delete failed')
                connection.commit()

    @classmethod
    def get(self, user_id, project_id, process_id, xml_file_link):
        query = """SELECT comment_on.id, comment_on.project_id, comment_on.xml_file_link, comment_on."content", comment_on.create_at,
                        bpe_user.id, bpe_user.email, bpe_user.phone, bpe_user.avatar
                    FROM public.comment_on
                        JOIN public.bpe_user ON comment_on.user_id=bpe_user.id
                    WHERE comment_on.user_id=%s AND comment_on.project_id=%s AND comment_on.process_id=%s AND comment_on.xml_file_link=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (user_id, project_id, process_id, xml_file_link,))
                return list_tuple_to_dict(["id", "project_id", "process_id", "xml_file_link", "content", "create_at", "user_id", "email", "phone", "avatar"], cursor.fetchall())

    @classmethod
    def get_by_bpmn_file(self, project_id, process_id, xml_file_link):
        query = """SELECT comment_on.id, comment_on.project_id, comment_on.xml_file_link, comment_on."content", comment_on.create_at,
                        bpe_user.id, bpe_user.email, bpe_user.phone, bpe_user.avatar
                    FROM public.comment_on
                        JOIN public.bpe_user ON comment_on.user_id=bpe_user.id
                    WHERE project_id=%s AND process_id=%s AND xml_file_link=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (project_id, process_id, xml_file_link,))
                result = []
                for record in cursor.fetchall():
                    cmt = dict(
                        zip(["id", "project_id", "process_id", "xml_file_link", "content", "create_at"], record[:5]))
                    user = dict(
                        zip(["id", "email", "phone", "avatar"], record[5:]))
                    cmt["author"] = user
                    result.append(cmt)
                return result

    @classmethod
    def get_by_user(self, user_id):
        query = """SELECT comment_on.id, comment_on.project_id, comment_on.xml_file_link, comment_on."content", comment_on.create_at,
                        bpe_user.id, bpe_user.email, bpe_user.phone, bpe_user.avatar
                    FROM public.comment_on
                        JOIN public.bpe_user ON comment_on.user_id=bpe_user.id
                    WHERE user_id=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (user_id,))
                result = []
                for record in cursor.fetchall():
                    cmt = dict(
                        zip(["id", "project_id", "xml_file_link", "content", "create_at"], record[:5]))
                    user = dict(
                        zip(["id", "email", "phone", "avatar"], record[5:]))
                    cmt["author"] = user
                    result.append(cmt)
                return result
