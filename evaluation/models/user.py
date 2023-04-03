from django.db import models


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
        user = cls(password=password, email=email,
                   name=name, phone=phone, avatar=avatar)
        return user
