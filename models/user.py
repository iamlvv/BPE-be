from .utils import *


class User:
    id = 0
    password = ""
    email = ""
    name = ""
    phone = ""
    avatar = ""
    verified = False

    def __init__(self, **kwargs):
        for k in kwargs:
            getattr(self, k)

        vars(self).update(kwargs)

    # def __init__(self, **kwargs):
    #     for arg in ["id", "password", "email", "name", "phone", "avatar", "verified"]:
    #         value = kwargs.pop(arg, None)
    #         setattr(self, arg, value)

    #     if kwargs:
    #         invalid_args = ", ".join(kwargs)
    #         raise ValueError("Invalid keyword argument(s): %s" %
    #                          (invalid_args,))

    @classmethod
    def create(self, hash_password, email, name, phone, avatar, verified=False):
        query = """INSERT INTO public.bpe_user
                ("password", email, "name", phone, avatar, verified)
                VALUES(%s, %s, %s, %s, %s, %s)
                RETURNING id, "password", email, "name", phone, avatar, verified;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (hash_password, email,
                                       name, phone, avatar, str(verified),))
                connection.commit()
                result = cursor.fetchone()
                return User(id=result[0], email=result[2], password=result[1])
        except:
            connection.rollback()

    @classmethod
    def change_password(self, email, new_hash_password):
        query = """UPDATE public.bpe_user
                    SET "password"=%s
                    WHERE email=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (new_hash_password, email,))
                connection.commit()
        except:
            connection.rollback()

    @classmethod
    def verify(self, email):
        query = """UPDATE public.bpe_user
                    SET verified=true
                    WHERE email=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                # updated_row = cursor.rowcount
                # if updated_row == 0:
                #     raise Exception("Email doesn't exist")
                connection.commit()
        except:
            connection.rollback()

    @classmethod
    def verify_token(self, id, email, hash_password):
        query = """SELECT id
                    FROM public.bpe_user
                    WHERE email=%s and id=%s and password=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email, id, hash_password,))
                result = cursor.fetchall()
                if len(result) == 0:
                    raise Exception('Token invalid')
        except:
            connection.rollback()

    @classmethod
    def get_by_email(self, email):
        query = """SELECT id, email, password, verified
                    FROM public.bpe_user
                    WHERE email=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                if result == None:
                    raise Exception('Email is incorrect')
                if result[-1]:
                    raise Exception('Your account was verified')
                return User(id=result[0], email=result[1], password=result[2])
        except:
            connection.rollback()

    @classmethod
    def get_by_email_permanently(self, email):
        query = """SELECT id, email, password
                    FROM public.bpe_user
                    WHERE email=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                if result == None:
                    raise Exception('Email is incorrect')
                return User(id=result[0], email=result[1], password=result[2])
        except:
            connection.rollback()

    @classmethod
    def get(self, email, hash_password):
        query = """SELECT id, email, password, verified
                    FROM public.bpe_user
                    WHERE email=%s and password=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email, hash_password,))
                result = cursor.fetchone()
                if result == None:
                    raise Exception('Email or password is incorrect')
                if not result[-1]:
                    raise Exception('Your account has not been verified')
                return User(id=result[0], email=result[1], password=result[2])
        except:
            connection.rollback()

    @classmethod
    def get_all(self):
        query = """SELECT id, email, "name", phone, avatar
                    FROM public.bpe_user;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(["id", "email", "name", "phone", "avatar"], result)
        except:
            connection.rollback()

    @classmethod
    def get_by_id(self, id):
        query = """SELECT name, email, phone, avatar
                    FROM public.bpe_user
                    WHERE id=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                result = cursor.fetchone()
                return User(name=result[0], email=result[1], phone=result[2], avatar=result[3])
        except:
            connection.rollback()

    @classmethod
    def get_many(self, user_ids):
        query = f"""SELECT name, phone, avatar
                    FROM public.bpe_user
                    WHERE id IN ({",".join(str(user_id) for user_id in user_ids)});
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(('name', 'phone', 'avatar'), result)
        except:
            connection.rollback()

    @classmethod
    def check_exist(self, email):
        query = """SELECT id
                    FROM public.bpe_user
                    WHERE email=%s;
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                return result != None
        except:
            connection.rollback()

    @classmethod
    def search(self, s, email):
        query = f"""SELECT id, email, name, phone, avatar
                    FROM public.bpe_user
                    WHERE email LIKE '%{s}%' AND email!='{email}';
                """
        connection = DatabaseConnector.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return list_tuple_to_dict(('id', 'email', 'name', 'phone', 'avatar'), result)
        except:
            connection.rollback()
