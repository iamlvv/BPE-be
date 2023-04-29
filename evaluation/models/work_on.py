from .utils import *
from .user import User
from .constant import Role


class WorkOn(models.Model):
    user_id = models.BigIntegerField()
    project_id = models.BigIntegerField()
    role = models.IntegerField()

    class Meta:
        db_table = "work_on"
        unique_together = (('user_id', 'project_id'),)

    @classmethod
    def insert(self, user_id, project_id, role):
        self(user_id=user_id, project_id=project_id, role=role).save()

    @classmethod
    def insert_many(self, user_id, project_id, role):
        self.objects.bulk_create(
            [WorkOn(user_id=i, project_id=project_id, role=role) for i in user_id])

    @classmethod
    def update_role(self, user_id, project_id, new_role):
        self.objects.filter(
            user_id=user_id, project_id=project_id).update(role=new_role)

    @classmethod
    def update_many_role(self, user_ids, project_id, new_role):
        self.objects.filter(
            user_id__in=user_ids, project_id=project_id).update(role=new_role)

    @classmethod
    def delete_many(self, user_id, project_id):
        self.objects.filter(user_id__in=user_id,
                            project_id=project_id).delete()

    @classmethod
    def get_all_project_by_user_id(self, user_id):
        return list(self.objects.filter(user_id=user_id).values())

    @classmethod
    def get_all_user_id_by_project_id(self, project_id):
        user_ids = [i.user_id for i in self.objects.filter(
            project_id=project_id)]
        return User.get_many(user_ids)

    @classmethod
    def get_all_project_id(self, user_id):
        return [i.project_id for i in self.objects.filter(user_id=user_id)]

    @classmethod
    def get_role_by_user_id(self, user_id, project_id):
        try:
            result = self.objects.get(user_id=user_id, project_id=project_id)
            return result.role
        except Exception:
            return -1

    @classmethod
    def is_not_exists(self, user_id, project_id):
        return self.objects.filter(user_id__in=user_id, project_id=project_id).count() == 0

    @classmethod
    def is_exists(self, user_id, project_id):
        result = self.objects.filter(
            user_id__in=user_id, project_id=project_id).count()
        return len(user_id) == result

    @classmethod
    def is_project_owner(self, user_id, project_id):
        try:
            result = self.objects.get(user_id=user_id, project_id=project_id)
            return result.role == Role.OWNER.value
        except Exception:
            return False

    @classmethod
    def can_edit(self, user_id, project_id):
        try:
            result = self.objects.get(user_id=user_id, project_id=project_id)
            return result.role in [Role.OWNER.value, Role.CAN_EDIT.value]
        except Exception:
            return False

    @classmethod
    def can_share(self, user_id, project_id):
        try:
            result = self.objects.get(user_id=user_id, project_id=project_id)
            return result.role in [Role.OWNER.value, Role.CAN_EDIT.value, Role.CAN_SHARE.value]
        except Exception:
            return False

    @classmethod
    def can_view(self, user_id, project_id):
        try:
            result = self.objects.get(user_id=user_id, project_id=project_id)
            return result.role in [Role.OWNER.value, Role.CAN_EDIT.value, Role.CAN_SHARE.value, Role.CAN_VIEW.value]
        except Exception:
            return False
