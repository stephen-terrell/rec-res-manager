from src.event.api.alert_event import AlertEvent


def handler(event, context):
    event_handler = AlertEvent(event=event, context=context)

    event_handler.handle()


if __name__ == '__main__':
    handler({}, {})
