import hashlib
import time
from datetime import datetime

from django.db import models
from django.http import JsonResponse
import uuid


class User(models.Model):
    password = models.CharField(max_length=8, null=False)
    email = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10, unique=True, null=True)
    avatar = models.CharField(max_length=50)

    class Meta:
        db_table = "bpe_user"

    @classmethod
    def create(cls, password, email, name, phone, avatar):
        user = cls(password=password, email=email, name=name, phone=phone, avatar=avatar)
        return user


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


class BPMNFile(models.Model):
    xml_file_link = models.CharField(unique=True, max_length=500, primary_key=True)
    project_id = models.IntegerField(unique=True)
    version = models.CharField(max_length=10)
    last_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bpmn_file"
        unique_together = (('xml_file_link', 'project_id'),)

    @classmethod
    def create(cls, xml_file_link, project_id, version, last_saved):
        bpmn_file = cls(xml_file_link=xml_file_link, project_id=project_id, version=version, last_saved=last_saved)
        return bpmn_file

    @classmethod
    def insert(cls, xml_file_link, project_id):
        version = str(uuid.uuid1())[:8]

        bpmn_file = cls.create(xml_file_link, project_id, version, datetime.now())
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
        bpmn_files = list(BPMNFile.objects.filter(project_id=project_id).values())
        return JsonResponse(bpmn_files, safe=False)
