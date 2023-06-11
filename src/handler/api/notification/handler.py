from src.event.api.notification.event import NotificationEvent


def handler(event, context):
    event_handler = NotificationEvent(event, context)

    return event_handler.handle()
