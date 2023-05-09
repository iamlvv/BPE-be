from .utils import *


class BPMNFile:
    xml_file_link = ""
    project_id = 0
    version = ""
    last_saved = datetime.now()

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    @classmethod
    def create(cls, xml_file_link, project_id, version):
        query = f"""INSERT INTO public.bpmn_file
                    (xml_file_link, project_id, "version", last_saved)
                    VALUES('{xml_file_link}', {project_id}, '{version}', NOW());
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def update_version(self, project_id, version):
        query = f"""UPDATE public.bpmn_file
                    SET last_saved=NOW()
                    WHERE project_id={project_id} AND version='{version}';
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

    @classmethod
    def get_all(cls):
        query = f"""SELECT xml_file_link, project_id, "version", last_saved
                    FROM public.bpmn_file;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return list_tuple_to_dict(["xml_file_link", "project_id", "version", "last_saved"], result)

    @classmethod
    def get_by_version(cls, project_id, version):
        query = f"""SELECT xml_file_link, "version", last_saved
                    FROM public.bpmn_file
                    WHERE project_id={project_id} AND version='{version}';
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result == None:
                raise Exception("version doesn't exist")
            return dict(zip(["xml_file_link", "version", "last_saved"], result))

    @classmethod
    def get_by_project(cls, project_id):
        query = f"""SELECT xml_file_link, "version", last_saved
                    FROM public.bpmn_file
                    WHERE project_id={project_id};
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return list_tuple_to_dict(["xml_file_link", "version", "last_saved"], result)

    @classmethod
    def delete(self, project_id, version):
        query = f"""DELETE FROM public.bpmn_file
                    WHERE version='{version}' AND project_id={project_id}
                    RETURNING xml_file_link;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            updated_row = cursor.rowcount
            if updated_row == 0:
                raise Exception("version doesn't exist")
            connection.commit()
            return cursor.fetchone()[0]

    @classmethod
    def delete_oldest_version(self, project_id):
        query = f"""DELETE FROM public.bpmn_file
                    WHERE project_id={project_id}
                        AND last_saved=(SELECT MIN(last_saved) FROM public.bpmn_file WHERE project_id={project_id});
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
