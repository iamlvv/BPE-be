from models.notification import Notification


class NotificationUseCase_Get:
    @classmethod
    def getAllNotifications(cls, userId, page, limit, isStarred, keyword=None):
        notifications = Notification.getAllNotifications(
            userId, page, limit, isStarred, keyword
        )
        if notifications is None:
            return None
        return notifications


class NotificationUseCase_Update:
    @classmethod
    def deleteNotification(cls, notificationIdList, deletedAt):
        return Notification.deleteNotification(notificationIdList, deletedAt)

    @classmethod
    def starNotification(cls, notificationId, isStarred):
        return Notification.starNotification(notificationId, isStarred)

    @classmethod
    def readNotification(cls, notificationId):
        return Notification.readNotification(notificationId)


class NotificationUseCase_Insert:
    @classmethod
    def insertNewNotification(
        cls, userId, content, createdAt, isDeleted, isStarred, isRead
    ):
        notification = Notification.insertNewNotification(
            userId, content, createdAt, isDeleted, isStarred, isRead
        )
        if notification is None:
            return None
        return notification


class NotificationUseCase(
    NotificationUseCase_Get, NotificationUseCase_Insert, NotificationUseCase_Update
):
    pass
