import json
from .utils import *


class EvaluatedResult:
    xml_file_link = ""
    project_id = 0
    name = ""
    result = ""
    description = ""
    create_at = datetime.now()

    @classmethod
    def insert(self, xml_file_link, project_id, name, result, description):
        query = """INSERT INTO public.evaluated_result
                    (xml_file_link, project_id, "name", "result", description, create_at)
                    VALUES(%s, %s, %s, %s::jsonb, %s, %s, %s, %s, NOW());
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (xml_file_link, project_id, name, json.dumps(result), description,))
            connection.commit()

    @classmethod
    def get_result_by_bpmn_file(self, xml_file_link, project_id):
        query = """SELECT "name", "result", description, create_at
                    FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (xml_file_link, project_id,))
            return list_tuple_to_dict(["name", "result", "description", "create_at"], cursor.fetchall())

    @classmethod
    def get(self, xml_file_link, project_id, name):
        query = """SELECT "name", "result", description, create_at
                    FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s AND "name"=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (xml_file_link, project_id, name,))
            return list_tuple_to_dict(["name", "result", "description", "create_at"], cursor.fetchall())[0]

    @classmethod
    def delete(self, xml_file_link, project_id, name):
        query = """DELETE FROM public.evaluated_result
                    WHERE xml_file_link=%s AND project_id=%s AND "name"=%s;
                """
        connection = DatabaseConnector.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query, (xml_file_link, project_id, name,))
            if cursor.rowcount == 0:
                raise Exception("result doesn't exist")
            connection.commit()
