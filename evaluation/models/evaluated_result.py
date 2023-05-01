from .utils import *


class EvaluatedResult(models.Model):
    xml_file_link = models.TextField()
    project_id = models.BigIntegerField()
    name = models.CharField(max_length=200, null=False, primary_key=True)
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
    def insert(self, xml_file_link, project_id, name, result, description, project_start_time, base_time_unit, base_currency_unit):
        result = self(
            xml_file_link=xml_file_link,
            project_id=project_id,
            name=name,
            result=result,
            description=description,
            project_start_time=project_start_time,
            base_time_unit=base_time_unit,
            base_currency_unit=base_currency_unit,
            create_at=datetime.now()
        )
        result.save()

    @classmethod
    def get_result_by_bpmn_file(self, xml_file_link, project_id):
        result = self.objects.filter(
            project_id=project_id, xml_file_link=xml_file_link
        ).values(
            'name',
            'result',
            'description',
            'project_start_time',
            'base_time_unit',
            'base_currency_unit',
            'create_at'
        )
        return list(result)

    @classmethod
    def get(self, xml_file_link, project_id, name):
        result = self.objects.filter(
            project_id=project_id, xml_file_link=xml_file_link, name=name
        ).values(
            'name',
            'result',
            'description',
            'project_start_time',
            'base_time_unit',
            'base_currency_unit',
            'create_at'
        )
        if len(result) == 0:
            raise Exception("result doesn't exist")
        return list(result)[0]

    @classmethod
    def delete(self, xml_file_link, project_id, name):
        obj = self.objects.filter(project_id=project_id,
                                  xml_file_link=xml_file_link, name=name)
        if len(obj) == 0:
            raise Exception("result doesn't exist")

        obj.delete()
