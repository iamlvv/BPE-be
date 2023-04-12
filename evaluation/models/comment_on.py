from .utils import *


class CommentOn(models.Model):
    user_id = models.BigIntegerField()
    project_id = models.BigIntegerField()
    xml_file_link = models.CharField(max_length=255)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment_on"
        unique_together = (('user_id', 'project_id', 'xml_file_link'),)
