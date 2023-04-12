from evaluation.models.user import User
from evaluation.auth.jwt import *
from .utils import *


class UserUsecase:
    @classmethod
    def create(self, password, email, name, phone, avatar):
        User.create(hash_password(password), email, name, phone, avatar)

    @classmethod
    def signin(self, email, password):
        result = User.get(email, hash_password(password))
        return encode({
            "id": result.id,
            "email": result.email,
            "password": result.password
        })

    @classmethod
    def signup(self, password, email, name, phone, avatar):
        if not UserUsecase.check_exist(email):
            UserUsecase.create(password, email, name, phone, avatar)
            return "Signup successfully"
        else:
            return "Account exist"

    @classmethod
    def get(self, token):
        id = get_id_from_token(token)
        user = User.get_by_id(id)
        return {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar
        }

    @classmethod
    def get_all(self):
        return list(User.objects.values())

    @classmethod
    def get_many(self, user_ids):
        return User.get_many(user_ids)

    @classmethod
    def check_exist(self, email):
        return User.check_exist(email)
