from .utils import *


class CommentOn(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    project_id = models.BigIntegerField()
    xml_file_link = models.CharField(max_length=255)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment_on"
        unique_together = (('id', 'user_id', 'project_id', 'xml_file_link'),)

    @classmethod
    def insert(self, user_id, project_id, xml_file_link, content):
        cmt = self(user_id=user_id, project_id=project_id,
                   xml_file_link=xml_file_link, content=content)
        cmt.save()

    @classmethod
    def update(self, id, content):
        updated = self.objects.filter(id=id).update(content=content)
        if updated == 0:
            raise Exception('update failed')

    @classmethod
    def owner(self, user_id, project_id, xml_file_link, id):
        return len(self.objects.filter(user_id=user_id, project_id=project_id, xml_file_link=xml_file_link, id=id)) > 0

    @classmethod
    def delete(self, id):
        obj = self.objects.filter(id=id)
        if len(obj) == 0:
            raise Exception('delete failed')
        obj.delete()

    @classmethod
    def get(self, user_id, project_id, xml_file_link):
        obj = self.objects.filter(user_id=user_id, project_id=project_id,
                                  xml_file_link=xml_file_link).values()
        return list(obj)

    @classmethod
    def get_by_bpmn_file(self, project_id, xml_file_link):
        obj = self.objects.filter(project_id=project_id,
                                  xml_file_link=xml_file_link).values()
        return list(obj)

    @classmethod
    def get_by_user(self, user_id):
        obj = self.objects.filter(user_id=user_id).values()
        return list(obj)
