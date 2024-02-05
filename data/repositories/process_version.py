from data.repositories.utils import *


class ProcessVersion:
    xml_file_link = ""
    project_id = 0
    process_id = 0
    version = ""
    num = 0
    last_saved = datetime.now()

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    @classmethod
    def create(cls, xml_file_link, project_id, process_id, version):
        query = f"""INSERT INTO public.process_version
                    (xml_file_link, project_id, process_id, "version", num, last_saved)
                    VALUES('{xml_file_link}', {project_id}, {process_id}, '{version}',
                        CAST((SELECT CASE WHEN MAX(num) IS NULL THEN 0 ELSE MAX(num) END
                            FROM public.process_version
                            WHERE project_id={project_id} AND process_id={process_id})
                            AS INT)+1,
                    NOW());
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
    def update_version(cls, project_id, process_id, version):
        query = f"""UPDATE public.process_version
                    SET last_saved=NOW()
                    WHERE project_id={project_id} AND process_id={process_id} AND version='{version}';
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
    def get_all(cls):
        query = f"""SELECT xml_file_link, project_id, process_id, "version", num, last_saved
                    FROM public.process_version;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(
                    [
                        "xml_file_link",
                        "project_id",
                        "process_id",
                        "version",
                        "num",
                        "last_saved",
                    ],
                    result,
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_by_version(cls, project_id, process_id, version):
        query = f"""SELECT xml_file_link, "version", num, last_saved
                    FROM public.process_version
                    WHERE project_id={project_id} AND process_id={process_id} AND version='{version}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result is None:
                    raise Exception("version doesn't exist")
                return dict(
                    zip(["xml_file_link", "version", "num", "last_saved"], result)
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_by_process(cls, project_id, process_id):
        query = f"""SELECT xml_file_link, "version", num, last_saved
                    FROM public.process_version
                    WHERE project_id={project_id} AND process_id={process_id}
                    ORDER BY last_saved DESC;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                if result is None:
                    raise Exception("version doesn't exist")
                return list_tuple_to_dict(
                    ["xml_file_link", "version", "num", "last_saved"], result
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def delete(cls, project_id, process_id, version):
        query = f"""DELETE FROM public.process_version
                    WHERE version='{version}' AND project_id={project_id} AND process_id={process_id}
                    RETURNING xml_file_link;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                updated_row = cursor.rowcount
                if updated_row == 0:
                    raise Exception("version doesn't exist")
                connection.commit()
                return cursor.fetchone()[0]
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def delete_by_process(cls, project_id, process_id):
        query = f"""DELETE FROM public.process_version
                    WHERE AND project_id={project_id} AND process_id={process_id}
                    RETURNING xml_file_link;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                updated_row = cursor.rowcount
                if updated_row == 0:
                    raise Exception("version doesn't exist")
                connection.commit()
                return cursor.fetchall()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def delete_oldest_version(cls, project_id, process_id):
        query = f"""DELETE FROM public.process_version
                    WHERE project_id={project_id} AND process_id={process_id}
                        AND last_saved=(SELECT MIN(last_saved) FROM public.process_version 
                        WHERE project_id={project_id} AND process_id={process_id});
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)
