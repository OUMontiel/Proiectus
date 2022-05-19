from models.notification import NotificationModel


def notificationEntity(item: NotificationModel) -> dict:
    return {
        "id":  str(item.id),
        "sent_by":  item.sent_by,
        "received_by":  item.received_by,
        "description":  item.description,
        "viewed": item.viewed
    }


def notificationsEntity(entity, user_id) -> list:
    print(entity)
    return [notificationEntity(item) for item in entity if (user_id == item['received_by']) and (not item['viewed'])]


