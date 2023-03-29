from datetime import datetime

from django.db import models
from django.http import JsonResponse


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
    document_link = models.CharField(max_length=255)
    name = models.CharField(max_length=25)
    is_delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project"

    @classmethod
    def create(cls, document_link, name):
        project = cls(document_link=document_link, name=name, is_delete=False, create_at=datetime.now())
        return project

    @classmethod
    def insert(cls, document_link, name):
        project = cls.create(document_link, name)
        project.save()

    @classmethod
    def get_all(cls):
        data = list(Project.objects.values())
        return JsonResponse(data, safe=False)


class EvaluatedResult(models.Model):
    xml_file_link = models.CharField(max_length=500)
    project_id = models.IntegerField()
    total_task = models.IntegerField()
    optional_task = models.IntegerField()
    flexibility = models.FloatField()
    number_of_handled_task = models.IntegerField()
    exception_handling = models.IntegerField()
    quality = models.IntegerField()
    cycle_time = models.FloatField()
    number_of_unhandled_task = models.IntegerField()
    total_cost = models.FloatField()

    class Meta:
        db_table = "evaluated_result"

    @classmethod
    def create(cls, xml_file_link, project_id, total_task, optional_task, flexibility, number_of_handled_task,
               exception_handling, quality, cycle_time, number_of_unhandled_task, total_cost):
        result = cls(xml_file_link=xml_file_link,
                     project_id=project_id,
                     total_task=total_task,
                     optional_task=optional_task,
                     flexibility=flexibility,
                     number_of_handled_task=number_of_handled_task,
                     exception_handling=exception_handling,
                     quality=quality, cycle_time=cycle_time,
                     number_of_unhandled_task=number_of_unhandled_task,
                     total_cost=total_cost
                     )
        return result

    @classmethod
    def insert(cls, xml_file_link, project_id, total_task, optional_task, flexibility, number_of_handled_task,
               exception_handling, quality, cycle_time, number_of_unhandled_task, total_cost):
        evaluated_result = cls.create(xml_file_link, project_id, total_task, optional_task, flexibility,
                                      number_of_handled_task,
                                      exception_handling, quality, cycle_time, number_of_unhandled_task, total_cost)
        evaluated_result.save()

    @classmethod
    def save(cls, request):
        pass

class BPMNFile(models.Model):
    xml_file_link = models.CharField(unique=True, max_length=500)
    project_id = models.IntegerField(unique=True)
    version = models.IntegerField()
    last_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bpmn_file"

    @classmethod
    def create(cls, xml_file_link, project_id, version, last_saved):
        bpmn_file = cls(xml_file_link=xml_file_link, project_id=project_id, version=version, last_saved=last_saved)
        return bpmn_file

    @classmethod
    def insert(cls, xml_file_link, project_id, version):
        bpmn_file = cls.create(xml_file_link, project_id, version, datetime.now())
        bpmn_file.save()

    @classmethod
    def get_all(cls):
        bpmn_file = list(BPMNFile.objects.values())
        return JsonResponse(bpmn_file, safe=False)


