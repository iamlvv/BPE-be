from .utils import *


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
    def create(self, hash_password, email, name, phone, avatar):
        user = self(password=hash_password, email=email,
                    name=name, phone=phone, avatar=avatar)
        user.save()

    @classmethod
    def get(self, email, hash_password):
        result = self.objects.get(email=email, password=hash_password)
        return result

    @classmethod
    def get_by_id(self, id):
        user = self.objects.get(id=id)
        return user

    @classmethod
    def get_many(self, user_ids):
        return list(User.objects.filter(id__in=user_ids).values('name', 'phone', 'avatar'))

    @classmethod
    def check_exist(self, email):
        return len(self.objects.filter(email=email)) > 0
