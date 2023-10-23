from models.user import User
from smtp.email import Email
from threading import Thread
import uuid
from auth.jwt import encode
from .utils import *


class UserUsecase:
    @classmethod
    def create(self, password, email, name, phone, avatar, verified=False):
        return User.create(
            hash_password(password), email, name, phone, avatar, verified
        )

    @classmethod
    def signin(self, email, password):
        print("hihi")
        result = User.get(email, hash_password(password))
        print(
            encode(
                {"id": result.id, "email": result.email, "password": result.password}
            )
        )
        return encode(
            {"id": result.id, "email": result.email, "password": result.password}
        )

    @classmethod
    def signup(self, password, email, name, phone, avatar):
        if not UserUsecase.check_exist(email):
            result = UserUsecase.create(password, email, name, phone, avatar)
            Thread(
                target=Email.verify_account,
                args=(
                    email,
                    name,
                    encode({"id": result.id, "email": email, "password": password}),
                ),
            ).start()
            return {
                "id": result.id,
                "email": result.email,
                "name": result.name,
            }
        else:
            return "Account exist"

    @classmethod
    def verify_token(self, id, email, password):
        User.verify_token(id, email, hash_password(password))

    @classmethod
    def resend_email(self, email):
        user = User.get_by_email(email)
        Thread(
            target=Email.verify_account,
            args=(
                email,
                user.name,
                encode({"id": user.id, "email": email, "password": user.password}),
            ),
        ).start()
        return "Resend successfully"

    @classmethod
    def change_password(self, email, new_password):
        User.change_password(email, hash_password(new_password))

    @classmethod
    def reset_password(self, email):
        user = User.get_by_email_permanently(email)
        Thread(
            target=Email.reset_password,
            args=(
                email,
                user.name,
                encode({"id": user.id, "email": email, "password": user.password}),
            ),
        ).start()

    @classmethod
    def verify(self, email):
        user = User.verify(email)
        return user

    @classmethod
    def get(self, id):
        user = User.get_by_id(id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "avatar": user.avatar,
        }

    @classmethod
    def get_all(self):
        return User.get_all()

    @classmethod
    def get_many(self, user_ids):
        return User.get_many(user_ids)

    @classmethod
    def check_exist(self, email):
        return User.check_exist(email)

    @classmethod
    def search(self, s, email):
        return User.search(s, email)

    @classmethod
    def auth_with_google(self, email, picture, name):
        if self.check_exist(email):
            User.verify(email)
            result = User.get_by_email_permanently(email)
        else:
            password = str(uuid.uuid1())[:10]
            result = self.create(
                hash_password(password), email, name, "", picture, True
            )
        return encode(
            {"id": result.id, "email": result.email, "password": result.password}
        )
