from datetime import datetime
from django.db import models
from django.http import JsonResponse
import uuid


class BPMNFile(models.Model):
    xml_file_link = models.CharField(
        unique=True, max_length=500, primary_key=True)
    project_id = models.IntegerField(unique=True)
    version = models.CharField(max_length=10)
    last_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bpmn_file"
        unique_together = (('xml_file_link', 'project_id'),)

    @classmethod
    def create(cls, xml_file_link, project_id, version, last_saved):
        bpmn_file = cls(xml_file_link=xml_file_link, project_id=project_id,
                        version=version, last_saved=last_saved)
        return bpmn_file

    @classmethod
    def insert(cls, xml_file_link, project_id):
        version = str(uuid.uuid1())[:8]

        bpmn_file = cls.create(xml_file_link, project_id,
                               version, datetime.now())
        bpmn_file.save()

    @classmethod
    def get_all(cls):
        bpmn_files = list(BPMNFile.objects.values())
        return JsonResponse(bpmn_files, safe=False)

    @classmethod
    def get_by_version(cls, version):
        bpmn_files = list(BPMNFile.objects.filter(version=version).values())
        return JsonResponse(bpmn_files, safe=False)

    @classmethod
    def get_by_project(cls, project_id):
        bpmn_files = list(BPMNFile.objects.filter(
            project_id=project_id).values())
        return JsonResponse(bpmn_files, safe=False)
