from django.db import models


class EvaluatedResult(models.Model):
    xml_file_link = models.CharField(max_length=500, primary_key=True)
    project_id = models.IntegerField()
    result = models.JSONField()

    class Meta:
        db_table = "evaluated_result"
        unique_together = (('xml_file_link', 'project_id'),)

    @classmethod
    def create(cls, xml_file_link, project_id, result):
        result = cls(xml_file_link=xml_file_link,
                     project_id=project_id,
                     result=result
                     )
        return result

    @classmethod
    def insert(cls, xml_file_link, project_id, result):
        result = cls(xml_file_link=xml_file_link,
                     project_id=project_id,
                     result=result
                     )
        result.save()
