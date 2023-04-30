from src.event.process_user_config_event import ProcessUserConfigEvent


def handler(event, context):
    event_handler = ProcessUserConfigEvent(event=event, context=context)

    event_handler.handle()


if __name__ == "__main__":
    handler({}, {})
