from src.event.api.alert.event import AlertEvent


def handler(event, context):
    event_handler = AlertEvent(event=event, context=context)

    return event_handler.handle()
