from src.event.api.campground.alert.event import AlertEvent


def handler(event, context):
    event_handler = AlertEvent(event=event, context=context)

    return event_handler.handle()
