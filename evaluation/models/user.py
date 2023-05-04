from .utils import *


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=200, null=False)
    email = models.TextField(unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, null=True)
    avatar = models.TextField()
    verified = models.BooleanField()

    class Meta:
        db_table = "bpe_user"

    @classmethod
    def create(self, hash_password, email, name, phone, avatar, verified=False):
        user = self(password=hash_password, email=email,
                    name=name, phone=phone, avatar=avatar, verified=verified)
        user.save()
        return user.id

    @classmethod
    def verify(self, email):
        obj = self.objects.filter(email=email)
        if len(obj) == 0:
            raise Exception("Email doesn't exist")
        obj.update(verified=True)

    @classmethod
    def verify_token(self, id, email):
        try:
            result = self.objects.get(
                email=email, id=id)
        except:
            raise Exception('Token invalid')
        return result

    @classmethod
    def get_by_email(self, email):
        try:
            result = self.objects.get(
                email=email)
        except:
            raise Exception('Email is incorrect')
        if result.verified:
            raise Exception('Your account was verified')
        return result

    @classmethod
    def get_by_email_permanently(self, email):
        try:
            result = self.objects.get(
                email=email)
        except:
            raise Exception('Email is incorrect')
        return result

    @classmethod
    def get(self, email, hash_password):
        try:
            result = self.objects.get(
                email=email, password=hash_password)
        except:
            raise Exception('Email or password is incorrect')
        if result.verified == False:
            raise Exception('Your account has not been verified')
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

    @classmethod
    def search(self, s):
        obj = self.objects.filter(email__contains=s).values(
            'email', 'name', 'avatar')
        return list(obj)
