from django.db import models
from datetime import datetime
from django.http import JsonResponse


class Project(models.Model):
    document = models.CharField(max_length=255)
    name = models.CharField(max_length=25)
    is_delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

    class Meta:
        db_table = "project"

    @classmethod
    def create(cls, document, name, user_id):
        project = cls(document=document, name=name, is_delete=False, create_at=datetime.now(),
                      user_id=user_id)
        return project

    @classmethod
    def insert(cls, document, name, user_id):
        project = cls.create(document, name, user_id)
        project.save()

    @classmethod
    def get_all(cls):
        data = list(Project.objects.values())
        return JsonResponse(data, safe=False)
