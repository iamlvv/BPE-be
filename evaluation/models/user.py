from django.db import models
from evaluation.models.utils import *
from evaluation.auth.jwt import *


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10, unique=True, null=True)
    avatar = models.CharField(max_length=50)

    class Meta:
        db_table = "bpe_user"

    @classmethod
    def create(self, password, email, name, phone, avatar):
        user = self(password=hash_password(password), email=email,
                    name=name, phone=phone, avatar=avatar)
        user.save()

    @classmethod
    def login(self, email, password):
        result = self.objects.filter(
            email=email, password=hash_password(password))
        print(result)
        return encode({
            "id": result[0].id,
            "email": result[0].email,
            "password": result[0].password
        }) if len(result) > 0 else ""

    @classmethod
    def get(self, token):
        id = decode(token)["id"]
        return self.objects.get(id=id)

    @classmethod
    def check_exist(self, email):
        return len(self.objects.filter(email=email)) > 0
