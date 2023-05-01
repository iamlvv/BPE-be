from .utils import *
from django.db.models import Min, Max


class HistoryImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.BigIntegerField()
    xml_file_link = models.TextField()
    save_at = models.DateTimeField(auto_now_add=True)
    image_link = models.TextField()

    class Meta:
        db_table = "history_image"
        unique_together = (
            ('xml_file_link', 'project_id', 'save_at', 'image_link'),)

    @classmethod
    def insert(self, project_id, xml_file_link, image_link):
        image = self(xml_file_link=xml_file_link, project_id=project_id,
                     save_at=datetime.now(), image_link=image_link)
        image.save()

    @classmethod
    def get_all_image_by_bpmn_file(self, project_id, xml_file_link):
        objs = self.objects.filter(
            xml_file_link=xml_file_link, project_id=project_id).values('image_link', 'save_at')
        return list(objs)

    @classmethod
    def count_all_image_by_bpmn_file(self, project_id, xml_file_link):
        return self.objects.filter(
            xml_file_link=xml_file_link, project_id=project_id).count()

    @classmethod
    def delete(self, project_id, xml_file_link, image_link):
        self.objects.filter(project_id=project_id,
                            xml_file_link=xml_file_link, image_link=image_link).delete()

    @classmethod
    def delete_oldest(self, project_id, xml_file_link):
        images = self.objects.filter(project_id=project_id,
                                     xml_file_link=xml_file_link)
        if len(images) == 0:
            raise Exception("don't have any image")
        last_saved = images.aggregate(Min("save_at"))["save_at__min"]
        images.filter(save_at=last_saved).delete()

    @classmethod
    def dif_last_saved(self, project_id, xml_file_link):
        obj = self.objects.filter(
            xml_file_link=xml_file_link, project_id=project_id)
        if len(obj) == 0:
            return True
        last_saved = obj.aggregate(Max("save_at"))["save_at__max"]
        now = datetime.now()
        return last_saved + timedelta(seconds=10) < now
