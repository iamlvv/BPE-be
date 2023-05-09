from .utils import *


class HistoryImage:
    # id = models.BigAutoField(primary_key=True)
    project_id = 0
    xml_file_link = ""
    save_at = datetime.now()
    image_link = ""

    @classmethod
    def insert(self, project_id, xml_file_link, image_link):
        query = """INSERT INTO public.history_image
                    (xml_file_link, project_id, save_at, image_link)
                    VALUES(%s, %s, NOW(), %s);
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id, image_link,))
            connection.commit()

    @classmethod
    def get_all_image_by_bpmn_file(self, project_id, xml_file_link):
        query = """SELECT image_link, save_at
                    FROM public.history_image
                    WHERE xml_file_link=%s AND project_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id,))
            return list_tuple_to_dict(['image_link', 'save_at'], cursor.fetchall())

    @classmethod
    def count_all_image_by_bpmn_file(self, project_id, xml_file_link):
        query = """SELECT image_link, save_at
                    FROM public.history_image
                    WHERE xml_file_link=%s AND project_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id,))
            return len(cursor.fetchall())

    @classmethod
    def delete(self, project_id, xml_file_link, image_link):
        query = """DELETE FROM public.history_image
                    WHERE xml_file_link=%s AND project_id=%s AND image_link=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id, image_link,))
            connection.commit()

    @classmethod
    def delete_oldest(self, project_id, xml_file_link):
        query = """DELETE FROM public.history_image
                    WHERE xml_file_link=%s AND project_id=%s
                        AND save_at=(SELECT MIN(save_at) FROM public.history_image WHERE xml_file_link=%s AND project_id=%s);
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id,
                           xml_file_link, project_id,))
            connection.commit()

    @classmethod
    def dif_last_saved(self, project_id, xml_file_link):
        query = """SELECT MIN(save_at)
                    FROM public.history_image
                    WHERE xml_file_link=%s AND project_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (xml_file_link, project_id,))
            result = cursor.fetchone()
            if result == None or result[0] == None:
                return True
            last_saved = result[0]
            return last_saved + timedelta(seconds=10) < datetime.now()
