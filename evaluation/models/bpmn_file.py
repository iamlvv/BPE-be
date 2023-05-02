from .utils import *
from django.db.models import Min
from datetime import datetime


class BPMNFile(models.Model):
    xml_file_link = models.TextField()
    project_id = models.BigIntegerField()
    version = models.CharField(max_length=10)
    last_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bpmn_file"
        unique_together = (('xml_file_link', 'project_id'),)

    @classmethod
    def create(cls, xml_file_link, project_id, version):
        bpmn_file = cls(xml_file_link=xml_file_link, project_id=project_id,
                        version=version, last_saved=datetime.now())
        bpmn_file.save()
        return bpmn_file

    @classmethod
    def update_version(self, project_id, version):
        self.objects.filter(project_id=project_id, version=version).update(
            last_saved=datetime.now())

    @classmethod
    def get_all(cls):
        bpmn_files = list(BPMNFile.objects.values())
        return bpmn_files

    @classmethod
    def get_by_version(cls, project_id, version):
        bpmn_files = list(BPMNFile.objects.filter(
            project_id=project_id, version=version).values('xml_file_link', 'version', 'last_saved'))
        return bpmn_files

    @classmethod
    def get_by_project(cls, project_id):
        bpmn_files = list(BPMNFile.objects.filter(
            project_id=project_id).values('xml_file_link', 'version', 'last_saved'))
        return bpmn_files

    @classmethod
    def delete(self, project_id, version):
        obj = self.objects.filter(project_id=project_id, version=version)
        if len(obj) == 0:
            raise Exception("version doesn't exist")
        xml_file_link = obj[0].xml_file_link
        obj.delete()
        return xml_file_link

    @classmethod
    def delete_oldest_version(self, project_id):
        versions = self.objects.filter(project_id=project_id)
        if len(versions) == 0:
            raise Exception("don't have anyversion")
        last_saved = versions.aggregate(
            Min("last_saved"))['last_saved__min']
        self.objects.filter(project_id=project_id,
                            last_saved=last_saved).delete()
