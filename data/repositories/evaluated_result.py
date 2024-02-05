import json
from data.repositories.utils import *


class EvaluatedResult:
    xml_file_link = ""
    project_id = 0
    process_id = 0
    name = ""
    result = ""
    description = ""
    create_at = datetime.now()

    @classmethod
    def insert(cls, xml_file_link, project_id, process_id, name, result, description):
        query = """INSERT INTO public.evaluated_result
                    (xml_file_link, project_id, process_id, "name", "result", description, create_at)
                    VALUES(%s, %s, %s, %s, %s::jsonb, %s, NOW());
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        xml_file_link,
                        project_id,
                        process_id,
                        name,
                        json.dumps(result),
                        description,
                    ),
                )
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get_result_by_bpmn_file(cls, xml_file_link, project_id, process_id):
        query = """SELECT "name", "result", description, create_at
                    FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s AND process_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        xml_file_link,
                        project_id,
                        process_id,
                    ),
                )
                return list_tuple_to_dict(
                    ["name", "result", "description", "create_at"], cursor.fetchall()
                )
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def get(cls, xml_file_link, project_id, process_id, name):
        query = """SELECT "name", "result", description, create_at
                    FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s AND "name"=%s AND process_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        xml_file_link,
                        project_id,
                        name,
                        process_id,
                    ),
                )
                list_result = list_tuple_to_dict(
                    ["name", "result", "description", "create_at"], cursor.fetchall()
                )
                if len(list_result) == 0:
                    return {}
                return list_result[0]
        except Exception as e:
            connection.rollback()
            raise Exception(e)

    @classmethod
    def delete(cls, xml_file_link, project_id, process_id, name):
        query = """DELETE FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s AND "name"=%s AND process_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        xml_file_link,
                        project_id,
                        name,
                        process_id,
                    ),
                )
                if cursor.rowcount == 0:
                    raise Exception("result doesn't exist")
                connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception(e)
