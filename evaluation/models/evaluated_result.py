from .utils import *


class EvaluatedResult(models.Model):
    xml_file_link = models.CharField(max_length=255)
    project_id = models.BigIntegerField()
    name = models.CharField(max_length=100, null=False, primary_key=True)
    result = models.JSONField()
    description = models.TextField()
    project_start_time = models.DateTimeField()
    base_time_unit = models.FloatField()
    base_currency_unit = models.CharField(max_length=10, null=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "evaluated_result"
        unique_together = (('xml_file_link', 'project_id', 'name'),)

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
