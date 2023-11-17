from models.notification import Notification


class NotificationUseCase:
    @classmethod
    def getAllNotifications(cls, userId, page, limit, isStarred, keyword=None):
        notifications = Notification.getAllNotifications(
            userId, page, limit, isStarred, keyword
        )
        if notifications is None:
            return None
        return notifications

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

    @classmethod
    def deleteNotification(cls, notificationIdList, deletedAt):
        return Notification.deleteNotification(notificationIdList, deletedAt)

    @classmethod
    def starNotification(cls, notificationId, isStarred):
        return Notification.starNotification(notificationId, isStarred)

    @classmethod
    def readNotification(cls, notificationId):
        return Notification.readNotification(notificationId)
