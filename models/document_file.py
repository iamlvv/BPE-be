from .utils import *


class DocumentFile:
    document_link: str
    project_id: int
    last_saved: datetime

    @classmethod
    def create(cls, document_link, project_id):
        query = """INSERT INTO public.document_file
                    (document_link, project_id, last_saved)
                    VALUES(%s, %s, NOW());
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (document_link, project_id,))
                connection.commit()

    @classmethod
    def update(self, document_link):
        query = """UPDATE public.document_file
                    SET last_saved=NOW()
                    WHERE document_link=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (document_link,))
                connection.commit()

    @classmethod
    def get(self, project_id):
        query = """SELECT document_link, project_id, last_saved
                    FROM public.document_file
                    WHERE project_id=%s;
                """
        with DatabaseConnector.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (project_id,))
                result = cursor.fetchone()
                if result == None:
                    raise Exception('project_id incorrect')
                return {
                    'document_link': result[0],
                    'project_id': result[1],
                    'last_saved': result[2]
                }
